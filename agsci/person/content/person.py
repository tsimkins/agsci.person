from .. import personMessageFactory as _
from agsci.atlas.content.behaviors import IAtlasMetadata, IAtlasContact
from agsci.leadimage.content.behaviors import ILeadImageBase
from dexterity.membrane.content.member import IMember
from plone.app.content.interfaces import INameFromTitle
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item, Container
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implements, provider, implementer

# Person

# Set up fields for re-use in API output

contact_fields = ['email', 'venue', 'street_address', 'city', 'state', 'zip_code', 'phone_number', 'fax_number', 'primary_profile_url']

professional_fields = ['classifications', 'job_titles', 'bio', 'areas_expertise', 'education', ]

social_media_fields = ['twitter_url', 'facebook_url', 'linkedin_url', 'google_plus_url', ]

@provider(IFormFieldProvider)
class IPerson(IMember, IAtlasContact, ILeadImageBase):

    # Fieldsets

    model.fieldset(
        'contact',
        label=_(u'Contact Information'),
        fields=contact_fields,
    )
    
    model.fieldset(
        'professional',
        label=_(u'Professional Information'),
        fields=professional_fields,
    )

    model.fieldset(
        'social-media',
        label=_(u'Social Media'),
        fields=social_media_fields,
    )

    form.omitted('homepage', 'map_link', 'leadimage_full_width', 'leadimage_caption')
    form.mode(leadimage_show='hidden')
    form.order_after(leadimage='suffix')

    # Fields

    username = schema.TextLine(
        title=_(u"Penn State Username"),
        description=_(u"Of format 'xyz123'"),
        required=True,
    )

    first_name = schema.TextLine(
        title=_(u"First Name"),
        required=True,
    )

    middle_name = schema.TextLine(
        title=_(u"Middle Name"),
        required=False,
    )

    last_name = schema.TextLine(
        title=_(u"Last Name"),
        required=True,
    )

    suffix = schema.TextLine(
        title=_(u"Suffix"),
        required=False,
    )

    classifications = schema.List(
        title=_(u"Classifications"),
        required=True,
        value_type=schema.Choice(vocabulary="agsci.person.classifications"),
    )

    job_titles = schema.List(
        title=_(u"Job Titles"),
        value_type=schema.TextLine(required=True),
        required=True,
    )

    education = schema.List(
        title=_(u"Education"),
        value_type=schema.TextLine(required=True),
        required=False,
    )

    areas_expertise = schema.List(
        title=_(u"Areas of Expertise"),
        value_type=schema.TextLine(required=True),
        required=False,
    )

    twitter_url = schema.TextLine(
        title=_(u"Twitter URL"),
        required=False,
    )

    facebook_url = schema.TextLine(
        title=_(u"Facebook URL"),
        required=False,
    )

    linkedin_url = schema.TextLine(
        title=_(u"LinkedIn URL"),
        required=False,
    )

    google_plus_url = schema.TextLine(
        title=_(u"Google+ URL"),
        required=False,
    )

    primary_profile_url = schema.TextLine(
        title=_(u"Primary Profile URL"),
        description=_(u"URL of primary profile (if not Extension site)"),
        required=False,
    )


# Calculate "Title" as person name
# Based on http://davidjb.com/blog/2010/04/plone-and-dexterity-working-with-computed-fields/

class Person(Item):

    @property
    def title(self):

        fields = ['first_name', 'middle_name', 'last_name']
        names = [getattr(self, x, '') for x in fields]
    
        v = " ".join([x.strip() for x in names if x])
        
        if getattr(self, 'suffix', ''):
            v = "%s, %s" % (v, self.suffix.strip())

        return v

    def setTitle(self, value):
        return

    def getSortableName(self):
        fields = ['last_name', 'first_name', 'middle_name', ]
        return tuple([getattr(self, x, '') for x in fields])

    def getFieldTitlesAndValues(self, fields, schemas=[]):

        data = []
        
        for field_name in fields:

            field_schema = None
            
            for i in schemas:
                try:
                    field_schema = i.getDescriptionFor(field_name)
                except KeyError:
                    continue
                else:
                    break

            field_value = getattr(self, field_name, None)

            if field_schema and field_value:
                data.append({'title' : field_schema.title, 'value' : field_value})

        return data
        
    def getSocialMedia(self):
       
        return self.getFieldTitlesAndValues(social_media_fields, [IPerson,])


    def getMetadata(self):
    
        fields = ['classifications', 'county', 'atlas_category_level_1', 'atlas_category_level_2', 'atlas_category_level_3']
        
        return self.getFieldTitlesAndValues(fields, [IPerson, IAtlasMetadata, IAtlasContact])

class ITitleFromPersonUserId(INameFromTitle):
    def title():
        """Return a processed title"""

class TitleFromPersonUserId(object):
    implements(ITitleFromPersonUserId)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.username

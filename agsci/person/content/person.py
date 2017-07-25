from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserRoles
from dexterity.membrane.behavior.user import DxUserObject
from dexterity.membrane.content.member import IMember
from plone.app.content.interfaces import INameFromTitle
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implements, provider, implementer

from agsci.atlas.constants import ACTIVE_REVIEW_STATES
from agsci.atlas.permissions import *
from agsci.atlas.content.behaviors import IAtlasContact, IAtlasLocation, \
                                          IAtlasSocialMediaBase, social_media_fields
from agsci.leadimage.content.behaviors import ILeadImageBase

from .. import personMessageFactory as _

# Person

# Set up fields for re-use in API output

contact_fields = [
    'email', 'venue', 'street_address', 'city', 'state',
    'zip_code', 'latitude', 'longitude', 'phone_number',
    'fax_number', 'primary_profile_url', 'summary_report_frequency',
]

professional_fields = [
    'classifications', 'job_titles', 'hr_job_title', 'hr_admin_area',
    'hr_department', 'all_emails', 'sso_principal_name', 'bio',
    'education', 'areas_expertise', 'county',
]

@provider(IFormFieldProvider)
class IPerson(IMember, IAtlasContact, ILeadImageBase, IAtlasSocialMediaBase):

    __doc__ = "Person Information"

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

    form.omitted('homepage', 'map_link', 'leadimage_full_width',
                 'leadimage_caption', 'hr_job_title', 'hr_admin_area',
                 'hr_department', 'all_emails', 'sso_principal_name')
    form.mode(leadimage_show='hidden')
    form.order_after(leadimage='suffix')

    # Only allow Directory Editors to write to these fields
    form.write_permission(leadimage=ATLAS_DIRECTORY)
    form.write_permission(username=ATLAS_DIRECTORY)
    form.write_permission(classifications=ATLAS_DIRECTORY)
    form.write_permission(primary_profile_url=ATLAS_DIRECTORY)
    form.write_permission(latitude=ATLAS_DIRECTORY)
    form.write_permission(longitude=ATLAS_DIRECTORY)

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

    hr_job_title = schema.TextLine(
        title=_(u"HR Job Title"),
        required=False,
    )

    hr_admin_area = schema.TextLine(
        title=_(u"HR Admin Area"),
        required=False,
    )

    hr_department = schema.TextLine(
        title=_(u"HR Department"),
        required=False,
    )

    all_emails = schema.Tuple(
        title=_(u"All Penn State Email Addresses"),
        value_type=schema.TextLine(required=True),
        required=False,
    )

    sso_principal_name = schema.TextLine(
        title=_(u"SSO Principal Name"),
        required=False,
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

    primary_profile_url = schema.TextLine(
        title=_(u"Primary Profile URL"),
        description=_(u"URL of primary profile (if not Extension site)"),
        required=False,
    )

    summary_report_frequency = schema.Choice(
        title=_(u"Summary Report Frequency"),
        description=_(u"Frequency that reports will be emailed."),
        values=[u'Weekly', u'Daily'],
        default=u'Weekly',
        required=True,
    )

# Configuring default roles with Dexterity
# http://docs.plone.org/develop/plone/members/membrane.html#id11

DEFAULT_ROLES = ['Member']

@implementer(IMembraneUserRoles)
@adapter(IPerson)
class PersonDefaultRoles(DxUserObject):

    def getRolesForPrincipal(self, principal, request=None):

        # Check if person is active
        wftool = getToolByName(self.context, 'portal_workflow')

        # Get workflow state
        review_state = wftool.getInfoFor(self.context, 'review_state')

        # Validate that person is published
        if review_state in ['published',]:

            # Get classifications for person
            classifications = getattr(self.context, 'classifications', [])

            # If the person has classification, but isn't a volunteer, they're a Member
            if classifications and 'Volunteer' not in classifications:
                return DEFAULT_ROLES

        # Default to no default roles
        return []

# Calculate "Title" as person name
# Based on http://davidjb.com/blog/2010/04/plone-and-dexterity-working-with-computed-fields/

class Person(Item):

    exclude_schemas = [IAtlasLocation, IAtlasContact]

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

    def getProducts(self):
        portal_catalog = getToolByName(self, "portal_catalog")

        # Find the brains for the products where this person is listed as the owner or author

        as_owner = portal_catalog.searchResults({'object_provides' : 'agsci.atlas.content.IAtlasProduct',
                                                  'Owners' : self.username,
                                                })

        as_author = portal_catalog.searchResults({'object_provides' : 'agsci.atlas.content.IAtlasProduct',
                                                  'Authors' : self.username,
                                                })

        # Put the UIDs from those brains into the `uids` list
        uids = []

        uids.extend([x.UID for x in as_owner])
        uids.extend([x.UID for x in as_author])


        # Return the brains for those products.
        return portal_catalog.searchResults({'object_provides' : 'agsci.atlas.content.IAtlasProduct',
                                                'UID' : uids,
                                                'review_state' : ACTIVE_REVIEW_STATES,
                                                'sort_on' : 'sortable_title',
                                            })

    def ContentIssues(self):
        issues = [0,0,0,0]

        for p in self.getProducts():
            content_issues = p.ContentIssues

            if content_issues == (0,0,0):
                issues[3] = issues[3] + 1

            elif content_issues and isinstance(content_issues, tuple) and len(content_issues) == 3:
                for i in range(0,3):
                    if content_issues[i] > 0:
                        issues[i] = issues[i] + 1
                        break

        return tuple(issues)



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

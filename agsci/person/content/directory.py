from .. import personMessageFactory as _
from Products.CMFCore.utils import getToolByName
from agsci.common.utilities import toISO
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema

# Directory

class IDirectory(model.Schema):

    classifications = schema.List(
        title=_(u"Classifications"),
        description=_(u"Classifications (e.g. Faculty, Staff, etc.) for people in the directory."),
        value_type=schema.TextLine(required=True),
        required=False,
    )

class Directory(Container):

    def listPeople(self, modified=None):
        portal_catalog = getToolByName(self, 'portal_catalog')

        query = {'Type' : 'Person', 'sort_on' : 'sortable_title'}

        if modified:
            query['modified'] = {'range' : 'min', 'query' : modified}

        return map(lambda x: x.getObject(), portal_catalog.searchResults(query))


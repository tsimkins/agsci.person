from .. import personMessageFactory as _
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

    def listPeople(self):
        return self.listFolderContents({'Type' : 'Person', 'sort_on' : 'sortable_title'})


from plone.dexterity.content import Container
from plone.supermodel import model

# Directory

class IDirectory(model.Schema):
    pass

class Directory(Container):

    def listPeople(self):
        return self.listFolderContents({'Type' : 'Person', 'sort_on' : 'sortable_title'})


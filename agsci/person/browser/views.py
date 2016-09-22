from Products.Five import BrowserView
from zope.interface import implements, Interface
from agsci.atlas.browser.views import AtlasStructureView

class IPersonView(Interface):
    pass

class PersonView(AtlasStructureView):

    def getPersonProducts(self):
        return self.context.getProducts()

    @property
    def getTileColumns(self):
        return '4'

class DirectoryView(AtlasStructureView):

    @property
    def getTileColumns(self):
        return '5'

    @property
    def show_image(self):
        return False

    def getPeople(self, contentFilter={}):
        return self.portal_catalog.searchResults({'Type' : 'Person', 'sort_on' : 'sortable_title'})
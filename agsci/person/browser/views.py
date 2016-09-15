from Products.Five import BrowserView
from zope.interface import implements, Interface
from agsci.atlas.browser.views import AtlasStructureView

class IPersonView(Interface):
    pass
    
class PersonView(AtlasStructureView):

    def getPersonProducts(self):
    
        return self.portal_catalog.searchResults({'object_provides' : 'agsci.atlas.content.IAtlasProduct',
                                                  'Owners' : self.context.username,
                                                  'sort_on' : 'sortable_title',
                                                })        

    @property
    def getTileColumns(self):
        return '4'

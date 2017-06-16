from zope.interface import Interface
from DateTime import DateTime

from agsci.atlas.browser.views import AtlasStructureView
from agsci.api.api import BaseView

from ..content import LDAPInfo

import json

class IPersonView(Interface):
    pass

class PersonView(AtlasStructureView):

    def getPersonProducts(self):
        return self.context.getProducts()

    @property
    def getTileColumns(self):
        return '4'

    def isExpired(self):
        now = DateTime()
        expires = self.context.expires()

        if expires:
            return (self.context.expires() < now)

        return False


class PersonLDAPView(BaseView):
    caching_enabled = False
    default_data_format = 'json'

    @property
    def data(self, **kwargs):
        return LDAPInfo(self.context).lookup()


class DirectoryView(AtlasStructureView):

    @property
    def getTileColumns(self):
        return '5'

    @property
    def show_image(self):
        return False

    def getPeople(self, contentFilter={}):
        return self.portal_catalog.searchResults({'Type' : 'Person', 'sort_on' : 'sortable_title'})
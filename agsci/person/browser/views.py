from DateTime import DateTime
from zope.component.hooks import getSite
from zope.interface import Interface

from agsci.atlas.browser.views import AtlasStructureView
from agsci.atlas.browser.views.sync.fsd_person import SyncFSDPersonView
from agsci.api.api import BaseView

from ..content import LDAPInfo, LDAPPersonCreator

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

class ImportPersonView(SyncFSDPersonView):

    @property
    def username(self):
        return self.request.get('username', None)

    def importContent(self):

        if self.username:
            v = LDAPPersonCreator(self.username).content_importer

            item = self.createObject(self.import_path, v)

            self.finalize(item)

            rv = [
                json.loads(self.getJSON(item))
            ]

            return json.dumps(rv, indent=4, sort_keys=True)


    def requestValidation(self):

        # No username provided
        if not self.username:
            raise ValueError("No username provided.")

        # Grab the directory, and do some sanity checks before jumping to LDAP
        site = getSite()

        directory_type = "Directory"

        if 'directory' not in site.objectIds():
            raise KeyError("%s not found." % directory_type)

        context = site['directory']

        if context.Type() != directory_type:
            raise TypeError("Directory portal_type of %s not %s"  % (context.portal_type, directory_type))

        if self.username in context.objectIds():
            raise ValueError("%s already in directory." % self.username)

        return True

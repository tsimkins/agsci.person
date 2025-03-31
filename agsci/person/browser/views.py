from DateTime import DateTime
from zope.component.hooks import getSite
from zope.interface import Interface

from agsci.api.api import BaseView
from agsci.atlas.browser.views import AtlasStructureView
from agsci.atlas.browser.views.sync import SyncContentView
from agsci.atlas.utilities import SitePeople
from agsci.person.content.vocabulary import ClassificationsVocabulary

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

class DirectoryLDAPView(BaseView):
    caching_enabled = False
    default_data_format = 'json'

    @property
    def data(self, **kwargs):
        username = self.request.form.get('username', None)
        return LDAPInfo(self.context, username=username).lookup()

class DirectoryView(AtlasStructureView):

    @property
    def getTileColumns(self):
        return '5'

    @property
    def show_image(self):
        return False

    def getPeople(self, contentFilter={}):
        return self.portal_catalog.searchResults({'Type' : 'Person', 'sort_on' : 'sortable_title'})


class ImportPersonView(SyncContentView):

    validate_ip = False

    # Translation of old to new attribute names
    translation = [
        ('email', 'email'),
        ('get_id', 'username'),
    ]

    @property
    def import_path(self):
        return getSite()['directory']

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

    def importContent(self):

        if self.username:
            v = LDAPPersonCreator(self.username).content_importer

            item = self.createObject(self.import_path, v)

            self.finalize(item)

            rv = [
                json.loads(self.getJSON(item))
            ]

            return json.dumps(rv, indent=4, sort_keys=True)

    # Deactivate people who are expired and active.
    def deactivateExpiredPeople(self):

        sp = SitePeople()

        expired_active_people = sp.expired_active_people

        for r in expired_active_people:

            o = r.getObject()

            msg = 'Automatically deactivating %s (%s) based on expiration date.' % (r.Title, r.getId)

            self.log(msg)
            sp.wftool.doActionFor(o, 'deactivate', comment=msg)
            o.reindexObject()

        self.log("Deactivated %d people" % len(expired_active_people))

    @property
    def username(self):
        return self.request.get('username', None)


    def getId(self, v):
        return v.data.get_id

    def getRequestDataAsArguments(self, v, item=None):
        data = super(ImportPersonView, self).getRequestDataAsArguments(v, item=None)

        # Get old and new fields from translation, and add values for new fields
        # if they exist
        for (old_key, new_key) in self.translation:

            value = getattr(v.data, old_key)

            if value:
                data[new_key] = value

        return data

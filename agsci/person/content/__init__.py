from Products.CMFPlone.utils import safe_unicode
from urlparse import urlparse

import ldap
import re

from agsci.atlas.content.sync import SyncContentImporter

class LDAPInfo(object):

    hosts = [
        'ldap://dirapps.aset.psu.edu',
        'ldap://fps.psu.edu'
    ]

    attrs = [
        'cn', 'displayName', 'dn', 'eduPersonAffiliation', 'eduPersonNickname',
        'eduPersonPrimaryAffiliation', 'eduPersonPrincipalName', 'givenName',
        'mail', 'postalAddress', 'psAdminArea', 'psCampus', 'psDepartment',
        'psDirIDN', 'psMailHost', 'psMailID', 'psMailbox', 'psOfficeAddress',
        'psOfficeLocation', 'psOfficePhone', 'sn', 'telephoneNumber', 'title',
        'uid', 'uidNumber',
    ]

    def __init__(self, context):
        self.context = context

    @property
    def username(self):

        username = getattr(self.context, 'username', None)

        if username:
            return username

    def lookup(self):

        try:
            return self.ldap_lookup()
        except:
            pass

    def ldap_lookup(self):

        username = self.username

        if username:

            for host in self.hosts:

                con = ldap.initialize(host)

                if con.simple_bind():
                    base_dn = "dc=psu,dc=edu"

                    _filter = "(uid=%s)" % username

                    results = con.search_s( base_dn, ldap.SCOPE_SUBTREE, _filter, self.attrs )

                    for r in results:
                        (_id, data) = r

                        for (k,v) in data.iteritems():

                            if isinstance(v, (tuple, list)):
                                if len(v) == 1:
                                    data[k] = v[0]

                        data['ldap_host'] = self.ldap_host(host)

                        return data
        return {}

    def is_fps(self, _):
        return _.get('ldap_host', '') == 'fps.psu.edu'

    def get_phone_number(self, ldap_data):

        if self.is_fps(ldap_data):
            return ''

        phone_number = ldap_data.get('psOfficePhone', '')

        if not phone_number:
            _ = ldap_data.get('telephoneNumber', '')

            if _ and isinstance(_, (str, unicode)):

                _re = re.compile('^\s*\+1\s*(\d{3})[\s\-\.]*(\d{3})[\s\-\.]*(\d{4})\s*$')

                m = _re.match(_)

                if m:
                    phone_number = "-".join(m.groups())

        return phone_number

    def get_address(self, ldap_data):

        if self.is_fps(ldap_data):
            return ''

        # Office Address

        # Blank city/state/zip
        city = state = zip_code = ''

        # Get street address from LDAP data
        street_address = ldap_data.get('postalAddress', '').title()

        # Clean spurious UP in street address
        _up = '$UNIVERSITY PARK$'.title()
        street_address = street_address.replace(_up, '$')

        # Split on $
        street_address = street_address.split('$')

        # Try to extract city/state/zip
        if len(street_address) > 1:

            # Check last line for city, state ZIP
            _csz_re = re.compile("^(.*),\s*(..)\s+([\d\-]+)\s*")

            _csz = _csz_re.match(street_address[-1])

            if _csz:
                (city, state, zip_code) = _csz.groups()
                street_address = street_address[:-1]
                state = state.upper()

        # Join with <cr>
        street_address = "\n".join(street_address)

        # Strip
        street_address = street_address.strip()

        return (street_address, city, state, zip_code)

    def ldap_host(self, _):
        return urlparse(_).netloc

class LDAPPersonCreator(LDAPInfo):

    def __init__(self, psu_id=None):
        self.psu_id = psu_id

    @property
    def username(self):
        return self.psu_id

    @property
    def content_importer(self):

        ldap_data = self.lookup()

        if not ldap_data:
            raise ValueError(u"%s not found in LDAP." % self.username)

        # Names
        givenName = ldap_data.get('givenName', '').title()
        last_name = ldap_data.get('sn', '').title()

        if ' ' in givenName:
            first_name = " ".join(givenName.split()[0:-1])
            middle_name = givenName.split()[-1]
        else:
            first_name = givenName
            middle_name = ''

        # Phone
        phone_number = self.get_phone_number(ldap_data)

        # Email
        email = ldap_data.get('mail', '')

        # Office Address
        (street_address, city, state, zip_code) = self.get_address(ldap_data)

        # Job Titles
        job_titles = []

        job_title = ldap_data.get('title', '').title()

        if job_title:
            job_titles.append(safe_unicode(job_title))

        # Compile in data dict and feed to content importer object
        data = {
            'username' : safe_unicode(self.username),
            'get_id' : safe_unicode(self.username),
            'first_name' : safe_unicode(first_name),
            'middle_name' : safe_unicode(middle_name),
            'last_name' : safe_unicode(last_name),
            'phone_number' : safe_unicode(phone_number),
            'street_address' : safe_unicode(street_address),
            'email' : safe_unicode(email),
            'city' : safe_unicode(city),
            'state' : safe_unicode(state),
            'zip_code' : safe_unicode(zip_code),
            'job_titles' : job_titles,
            'product_type' : u'Person',
        }

        return SyncContentImporter(data)
import ldap

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

                        return data
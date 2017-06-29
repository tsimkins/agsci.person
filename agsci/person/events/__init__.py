# Update person when person edited
from agsci.atlas.events import assignOwnerPermission

from ..content import LDAPInfo

def onPersonEdit(context, event):

    setPersonUsername(context, event)

    setPersonLDAPInfo(context, event)

def setPersonUsername(context, event):

    username = getattr(context, 'username', '')

    if username:

        username = username.encode('utf-8')

        if username != context.getId():

            parent = context.aq_parent

            if username not in parent.objectIds():
                parent.manage_renameObjects(ids=[context.getId()], new_ids=[username])

        # Assign the person's username as the owner
        assignOwnerPermission(context, event)

        return username

def setPersonLDAPInfo(context, event):

    data = LDAPInfo(context).lookup()

    updated = False

    if data:

        fields = [
            ('hr_job_title', 'title'),
            ('hr_admin_area', 'psAdminArea'),
            ('hr_department', 'psDepartment'),
            ('all_emails', 'psMailID'),
            ('sso_principal_name', 'eduPersonPrincipalName'),
        ]

        for (plone_field_name, ldap_field_name) in fields:

            field_value = data.get(ldap_field_name, '')

            # Special case for alternate_emails, which need to be a list
            if plone_field_name in ['all_emails'] and field_value:
                if not isinstance(field_value, (list, tuple)):
                    field_value = (field_value,)

            current_value = getattr(context, plone_field_name, None)

            if current_value != field_value:
                setattr(context, plone_field_name, field_value)
                updated = True

        if updated:
            context.reindexObject()

    return updated
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

    if data:
        setattr(context, 'hr_job_title', data.get('title', ''))
        context.reindexObject()
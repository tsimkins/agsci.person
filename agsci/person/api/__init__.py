from agsci.api import BaseView, BaseContainerView
from dexterity.membrane.content.member import IMember
from ..content.person import IPerson

class DirectoryView(BaseContainerView):

    # Explicitly only list people
    def getContents(self):

        # Pass the result of `getModifiedCriteria` (reflecting a last modified date
        # based on an `updated` parameter passed in via the URL) to the `listPeople`
        # method.
        modified = self.getModifiedCriteria()

        return self.context.listPeople(modified)

class PersonView(BaseView):

    def getData(self):
        data = super(PersonView, self).getData()

        sd = self.getSchemaData(schemas=[IMember, IPerson], fields=['email'])

        data.update(sd)

        return data


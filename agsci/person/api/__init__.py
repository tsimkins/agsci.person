from agsci.api import BaseView, BaseContainerView
from dexterity.membrane.content.member import IMember
from ..content.person import IPerson

class DirectoryView(BaseContainerView):

    # Explicitly only list people
    def getContents(self):
        return self.context.listPeople()

class PersonView(BaseView):

    def getData(self):
        data = super(PersonView, self).getData()

        sd = self.getSchemaData(schemas=[IMember, IPerson], fields=['email'])

        data.update(sd)

        return data


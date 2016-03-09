from agsci.api import BaseView, BaseContainerView
from ..content.person import IPerson, contact_fields, professional_fields, social_media_fields

class DirectoryView(BaseContainerView):

    # Explicitly only list people
    def getContents(self):
        return self.context.listPeople()

class PersonView(BaseView):

    def getData(self):
        data = super(PersonView, self).getData()
        
        sd = self.getSchemaData(schemas=[IPerson,], fields=[])
        
        data.update(sd)

        return data


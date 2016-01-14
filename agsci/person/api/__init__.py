from agsci.api import BaseView, BaseContainerView
from ..content.person import IPerson, contact_fields, professional_fields, social_media_fields

class DirectoryView(BaseContainerView):

    # Explicitly only list people
    def getContents(self):
        return self.context.listPeople()

class PersonView(BaseView):

    # Configure data nested data (easier to read this way!)
    structures = {
        'name' : ['first_name', 'middle_name', 'last_name', 'suffix'],   
        'social_media' : social_media_fields,
        'contact' : contact_fields,
        'professional' : professional_fields,
    }

    def getData(self):
        data = super(PersonView, self).getData()
        
        sd = self.getStructuredData(schemas=(IPerson,), structures=self.structures)
        
        data.update(sd)

        return data


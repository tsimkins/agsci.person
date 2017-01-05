from agsci.api.api import BaseView, BaseContainerView
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

        # Add a 'job_title' field with the primary job title
        job_titles = sd.get('person_job_titles', [])

        if job_titles:
            sd['person_job_title'] = sd['short_description'] = job_titles[0] # Note *singular*

        # Split `street_address` into a list
        street_address = data.get('address', None)

        if isinstance(street_address, (list, tuple)):
            street_address = [x.strip() for x in street_address if x.strip()]
            sd['address'] = street_address[0:3] # First three lines only

        data.update(sd)

        return data


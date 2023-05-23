from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implementer

from agsci.atlas.utilities import SitePeople

# Directory classifications for people
@implementer(IVocabularyFactory)
class ClassificationsVocabulary(object):

    items = [
        'Faculty',
        'Educator',
        'Staff',
        'Director',
        'Associate Director',
        'Assistant Director of Programs',
        'Assistant Director for County Operations',
        'Client Relationship Manager',
        'Business Operations Manager',
        'Leadership Team',
        'Team Marketing Coordinator',
        'Volunteer',
    ]

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in self.items]
        )

@implementer(IVocabularyFactory)
class PersonClassificationsVocabulary(object):

    find_classifications = []

    def __call__(self, context):

        sp = SitePeople()

        people = sp.getValidPeople()

        filtered_people = [
            x.getObject() for x in people if set(x.Classifications) & set(self.find_classifications)
        ]

        return SimpleVocabulary(
            [SimpleTerm(x.username ,title=x.Title()) for x in filtered_people]
        )

class CRMVocabulary(PersonClassificationsVocabulary):

    find_classifications = [
        'Client Relationship Manager',
    ]

class BOMVocabulary(PersonClassificationsVocabulary):

    find_classifications = [
        'Business Operations Manager',
    ]

ClassificationsVocabularyFactory = ClassificationsVocabulary()
CRMVocabularyFactory = CRMVocabulary()
BOMVocabularyFactory = BOMVocabulary()

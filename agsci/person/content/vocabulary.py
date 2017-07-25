from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements

# Directory classifications for people
class ClassificationsVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        classifications = [
            'Faculty',
            'Educator',
            'Staff',
            'Director',
            'Associate Director',
            'Assistant Director of Programs',
            'Client Relations Manager',
            'Business Operations Manager',
            'Leadership Team',
            'Volunteer',
        ]

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in classifications]
        )

ClassificationsVocabularyFactory = ClassificationsVocabulary()
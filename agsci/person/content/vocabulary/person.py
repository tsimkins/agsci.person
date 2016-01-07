from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ..directory import IDirectory

states = ['PA', ]

from counties import counties

# Directory classifications for people
class ClassificationsVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        classifications = []

        for o in context.aq_chain:
    
            if IPloneSiteRoot.providedBy(o):
                break
    
            if IDirectory.providedBy(o):
                classifications = getattr(o, 'classifications', ['Faculty', 'Staff'])
                break

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in classifications]
        )


ClassificationsVocabularyFactory = ClassificationsVocabulary()


# Directory States for people
class StatesVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in states]
        )


StatesVocabularyFactory = StatesVocabulary()


# Directory Counties for people
class CountiesVocabulary(object):

    implements(IVocabularyFactory)
    
    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in counties]
        )


CountiesVocabularyFactory = CountiesVocabulary()
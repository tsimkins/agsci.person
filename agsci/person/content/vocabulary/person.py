from agsci.atlas.content.vocabulary import StaticVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from ..directory import IDirectory


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
class StatesVocabulary(StaticVocabulary):

    items = ['PA', ]


StatesVocabularyFactory = StatesVocabulary()
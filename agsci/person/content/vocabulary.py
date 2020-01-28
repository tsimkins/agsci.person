from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements

from agsci.atlas.utilities import SitePeople

# Directory classifications for people
class ClassificationsVocabulary(object):

    implements(IVocabularyFactory)

    items = [
        'Faculty',
        'Educator',
        'Staff',
        'Director',
        'Associate Director',
        'Assistant Director of Programs',
        'Client Relations Manager',
        'Business Operations Manager',
        'Leadership Team',
        'Team Marketing Coordinator',
        'Volunteer',
    ]

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in self.items]
        )

# Project / Program Team
class ProjectProgramTeamVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            (u'4275', u'Administrative Project'),
            (u'8000', u'4-H Youth Development: Base Unit Activity'),
            (u'8001', u'4-H Youth Development: Science'),
            (u'8002', u'4-H Youth Development: Volunteer Management & Development'),
            (u'8003', u'4-H Youth Development: Positive Youth Development'),
            (u'8100', u'Energy,Entreprenurship &CD:  Base Unit Activity'),
            (u'8101', u'New & Beginning Farmers'),
            (u'8102', u'Shale Gas'),
            (u'8103', u'Ag Entrepreneurship/ECD'),
            (u'8105', u'Leadership & Community Vitality'),
            (u'8201', u'Dairy Profitability & Sustainability'),
            (u'8301', u'Equine'),
            (u'8401', u'Livestock Profitability & Sustainability'),
            (u'8402', u'Farm Animal Welfare Team'),
            (u'8501', u'Poultry Profitability & Sustainability'),
            (u'8600', u'Field & Forage Crops'),
            (u'8601', u'Pesticide Education'),
            (u'8602', u'Farm Safety'),
            (u'8605', u'Master Watershed Steward'),
            (u'8700', u'Food Safety & Quality:  Base Unit Activity'),
            (u'8701', u'Industrial Food Safety & Quality'),
            (u'8702', u'Retail, Food Service, & Consumer Food Safety'),
            (u'8703', u'Food Safety Modernization Act'),
            (u'8800', u'Horticulture:  Base Unit Activity'),
            (u'8801', u'Green Industry & Infrastructure'),
            (u'8803', u'Tree Fruit Profitability & Sustainability'),
            (u'8804', u'Vegetable Profitability & Sustainability'),
            (u'8805', u'Master Gardener'),
            (u'8806', u'Grape Profitability & Sustainability'),
            (u'8900', u'Agronomy & Natural Resources:  Base Unit Activity'),
            (u'8901', u'Water Quality & Quantity'),
            (u'8902', u'Forestry & Wildlife'),
            (u'8903', u'Urban Forestry'),
            (u'8904', u'Bio-Energy'),
            (u'9000', u'Food, Family & Health:  Base Unit Activity'),
            (u'9001', u'Health and Wellness'),
            (u'9002', u'Family Well-Being'),
            (u'9003', u'Vector Borne Diseases'),
            (u'9100', u'Insect-Borne Disease Management (includes West Nile Virus)'),
        ]

        items.sort(key=lambda x:x[1])

        return SimpleVocabulary(
            [SimpleTerm(x[0] ,title=x[1]) for x in items]
        )

class HomeBudgetVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            u'0200437 BK10010',
            u'0200439 UP10010',
            u'0200466 BK10010',
            u'0200479 UP10010',
            u'0200482 UP10010',
            u'0400425 UP10010',
            u'0400429 UP10010',
            u'0400439 UP10010',
            u'0400449 UP10010',
            u'0400451 UP10010',
            u'0400479 UP10010',
            u'0400480 UP10010',
            u'0400482 UP10010',
            u'0400489 UP10010',
            u'0400490 UP10010',
            u'0400491 UP10010',
            u'0500401 UP10010',
            u'0500424 UP10010',
            u'0500429 UP10010',
            u'0500432 UP10010',
            u'0500439 UP10010',
            u'0500449 UP10010',
            u'0500455 UP10010',
            u'0500455 UP12160',
            u'0500459 UP10010',
            u'0500461 UP10010',
            u'0500462 UP10010',
            u'0500465 UP10010',
            u'0500474 UP10010',
            u'0500475 UP10010',
            u'0500476 UP10010',
            u'0500479 UP10010',
            u'0500480 UP10010',
            u'0500481 UP10010',
            u'0500482 UP10010',
            u'0500489 UP10010',
            u'0500490 UP10010',
            u'0500491 UP10010',
            u'0800484 UP10010',
        ]

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in items]
        )

class PersonClassificationsVocabulary(object):

    implements(IVocabularyFactory)

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
        'Client Relations Manager',
    ]

class BOMVocabulary(PersonClassificationsVocabulary):

    find_classifications = [
        'Business Operations Manager',
    ]

ClassificationsVocabularyFactory = ClassificationsVocabulary()
ProjectProgramTeamVocabularyFactory = ProjectProgramTeamVocabulary()
HomeBudgetVocabularyFactory = HomeBudgetVocabulary()
CRMVocabularyFactory = CRMVocabulary()
BOMVocabularyFactory = BOMVocabulary()
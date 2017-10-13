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

# Project / Program Team
class ProjectProgramTeamVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            ('8000', '4-H Youth Development: Base Unit Activity'),
            ('8001', '4-H Youth Development: Science'),
            ('8002', '4-H Youth Development: Volunteer Management & Development'),
            ('8003', '4-H Youth Development: Positive Youth Development'),
            ('8100', 'Energy,Entreprenurship &CD:  Base Unit Activity'),
            ('8101', 'New & Beginning Farmers'),
            ('8102', 'Shale Gas'),
            ('8103', 'Ag Entrepreneurship/ECD'),
            ('8201', 'Dairy Profitability & Sustainability'),
            ('8301', 'Equine'),
            ('8401', 'Livestock Profitability & Sustainability'),
            ('8402', 'Farm Animal Welfare Team'),
            ('8500', '8500 is Blank'),
            ('8501', 'Poultry Profitability & Sustainability'),
            ('8600', 'Field & Forage Crops'),
            ('8601', 'Pesticide Education'),
            ('8602', 'Farm Safety'),
            ('8700', 'Food Safety & Quality:  Base Unit Activity'),
            ('8701', 'Industrial Food Safety & Quality'),
            ('8702', 'Retail, Food Service, & Consumer Food Safety'),
            ('8703', 'Food Safety Modernization Act'),
            ('8800', 'Horticulture:  Base Unit Activity'),
            ('8801', 'Green Industry & Infrastructure'),
            ('8803', 'Tree Fruit Profitability & Sustainability'),
            ('8804', 'Vegetable Profitability & Sustainability'),
            ('8805', 'Master Gardener'),
            ('8806', 'Grape Profitability & Sustainability'),
            ('8900', 'Agronomy & Natural Resources:  Base Unit Activity'),
            ('8901', 'Water Quality & Quantity'),
            ('8902', 'Forestry'),
            ('8903', 'Urban Forestry'),
            ('8904', 'Bio-Energy'),
            ('9000', 'Food, Family & Health:  Base Unit Activity'),
            ('9001', 'Health and Wellness'),
            ('9002', 'Family Well-Being'),
            ('9100', 'Insect-Borne Disease Management (includes West Nile Virus)'),
        ]

        items.sort(key=lambda x:x[1])

        return SimpleVocabulary(
            [SimpleTerm(x[0] ,title=x[1]) for x in items]
        )

class HomeBudgetVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            '0200437 BK',
            '0200439 UP',
            '0200466 BK',
            '0200482 UP',
            '0400439 UP',
            '0400449 UP',
            '0400479 UP',
            '0400480 UP',
            '0400482 UP',
            '0400489 UP',
            '0400490 UP',
            '0400491 UP',
            '0402155 UP',
            '0402407 UP',
            '0500401 UP',
            '0500424 UP',
            '0500429 UP',
            '0500439 UP',
            '0500449 UP',
            '0500455 UP',
            '0500459 UP',
            '0500461 UP',
            '0500462 UP',
            '0500465 UP',
            '0500474 UP',
            '0500475 UP',
            '0500476 UP',
            '0500479 UP',
            '0500480 UP',
            '0500481 UP',
            '0500489 UP',
            '0500490 UP',
            '0500491 UP',
        ]

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in items]
        )

ClassificationsVocabularyFactory = ClassificationsVocabulary()
ProjectProgramTeamVocabularyFactory = ProjectProgramTeamVocabulary()
HomeBudgetVocabularyFactory = HomeBudgetVocabulary()
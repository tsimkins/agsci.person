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
            u'0500461 UP 10010',
            u'0500461 UP10010',
            u'0500462 UP 10010',
            u'0500462 UP10010',
            u'0500465 UP10010',
            u'0500474 UP10010',
            u'0500475 UP10010',
            u'0500476 UP10010',
            u'0500479 UP10010',
            u'0500480 UP10010',
            u'0500481 UP10010',
            u'0500482 UP10010',
            u'0500483 UP 10010',
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

class CostCenterVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            "2120110001",
            "2120302000",
            "2120302001",
            "2120310002",
            "2120310003",
            "2120602000",
            "2120610000",
            "2120702000",
            "2120705000",
            "2120710000",
            "2120710001",
            "2120802000",
            "2120805000",
            "2120810000",
            "2120902000",
            "2120905000",
            "2120910000",
            "2121002000",
            "2121005000",
            "2121010000",
            "2121102000",
            "2121105000",
            "2121110000",
            "2121202000",
            "2121205000",
            "2121210000",
            "2121302000",
            "2121305000",
            "2121310000",
            "2121402000",
            "2121405000",
            "2121410000",
            "2121502000",
            "2121602000",
            "2122010000",
            "2123002000",
            "2123102000",
            "2123202000",
            "2123302000",
            "2123402000",
            "2123502000",
            "2123602000",
            "2123702000",
            "2123802000",
            "2123902000",
            "6391310001",
            "6972910000",
            "8751705007",
            "8751705009",
            "8970210000"
        ]

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in items]
        )

class BudgetVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            "204-04",
            "204-29",
            "204-37",
            "204-39",
            "204-49",
            "204-66",
            "204-80",
            "204-82",
            "204-89",
            "204-90",
            "204-91",
            "404-20",
            "404-25",
            "404-29",
            "404-39",
            "404-49",
            "404-50",
            "404-51",
            "404-79",
            "404-80",
            "404-82",
            "404-89",
            "404-90",
            "404-91",
            "430-36",
            "504-01",
            "504-24",
            "504-25",
            "504-29",
            "504-38",
            "504-39",
            "504-49",
            "504-51",
            "504-55",
            "504-59",
            "504-61",
            "504-62",
            "504-65",
            "504-67",
            "504-74",
            "504-75",
            "504-76",
            "504-79",
            "504-80",
            "504-81",
            "504-82",
            "504-83",
            "504-89",
            "504-90",
            "504-91",
            "523-16",
            "545-22",
            "804-84",
            "971-72"
        ]

        return SimpleVocabulary(
            [SimpleTerm(x ,title=x) for x in items]
        )

class ProjectVocabulary(object):

    implements(IVocabularyFactory)

    def __call__(self, context):

        items = [
            (u'8301', u'Equine'),
            (u'4704', u'Management of the Brown Marmorated Stink Bug'),
            (u'4702', u'Conservation and Management of Pennsylvania Birds'),
            (u'4701', u'Forest Management and Social Values in Pennsylvania and the Mid-Atlantic Region'),
            (u'4677', u'Conifer Improvement to Increase Green Industry Sustainability and Resilience'),
            (u'4675', u'Cultural and Chemical Management of Invasive Plants and Roadside Vegetation'),
            (u'4674', u'Management Systems to Improve the Economic and Environmental Sustainability of Dairy Enterprises'),
            (u'4670', u'Fly Management in Animal Agriculture Systems and Impacts on Animal Health and Food Safety'),
            (u'8901', u'Water Quality &amp; Quantity'),
            (u'8900', u'Agronomy &amp; Natural Resources:  Base Unit Activity'),
            (u'8903', u'Urban Forestry'),
            (u'8902', u'Forestry &amp; Wildlife'),
            (u'3333', u'Research Administration (E&amp;G Funds)'),
            (u'4736', u'Industrial Hemp Production, Processing, and Marketing in the U.S.'),
            (u'4739', u'Specialty Crops and Food Systems:  Exploring Markets, Supply Chains and Policy Dimensions'),
            (u'8703', u'Food Safety Modernization Act'),
            (u'8702', u'Retail, Food Service, &amp; Consumer Food Safety'),
            (u'8701', u'Industrial Food Safety &amp; Quality'),
            (u'8602', u'Farm Safety'),
            (u'8600', u'Field &amp; Forage Crops'),
            (u'8601', u'Pesticide Education'),
            (u'8605', u'Master Watershed Steward'),
            (u'4656', u'National and International Dimensions of Leadership and Community Engagement'),
            (u'4653', u'Integrated Systems Research and Development in Automation and Sensors for Sustainability of Specialty Crops'),
            (u'XXXX', u'Teaching'),
            (u'4723', u'Improving Vegetable Production Systems Sustainability and Vegetable Quality'),
            (u'4722', u'Identifying and Creating a Conservation Easement Model to Conserve Working Forests'),
            (u'8804', u'Vegetable, Small Fruit &amp; Mushroom'),
            (u'8805', u'Master Gardener'),
            (u'8806', u'Grape &amp; Enology'),
            (u'8801', u'Green Industry &amp; Infrastructure'),
            (u'8803', u'Tree Fruit Profitability &amp; Sustainability'),
            (u'8201', u'Dairy Profitability &amp; Sustainability'),
            (u'9003', u'Vector-Borne Disease'),
            (u'9002', u'Family Well-Being'),
            (u'9001', u'Health &amp; Wellness'),
            (u'4627', u'Collaborative Potato Breeding and Variety Development Activities to Enhance Farm Sustainability in the Eastern US'),
            (u'4628', u'Multi-state Coordinated Evaluation of Winegrape Cultivars and Clones'),
            (u'4540', u'Multistate Research and Extension Coordination'),
            (u'4679', u'Sustainable Landscape Management within the Green Industry'),
            (u'4750', u'Biology, Etiology, and Management of Dollar Spot in Turfgrass'),
            (u'4757', u'Harnessing Chemical Ecology to Address Agricultural Pest and Pollinator Priorities'),
            (u'4625', u'Improving Economic and Environmental Sustainability in Tree-Fruit Production Through Changes in Rootstock Use'),
            (u'8501', u'Poultry Profitability &amp; Sustainability'),
            (u'9000', u'Food, Family &amp; Health:  Base Unit Activity'),
            (u'4633', u'Enhancing Rural Economic Opportunities, Community Resilience, and Entrepreneurship'),
            (u'4632', u'Integrated Onion Pest and Disease Management'),
            (u'4636', u'Mastitis Resistance to Enhance Dairy Food Safety'),
            (u'4275', u'ADM: Planning and Coordination'),
            (u'4743', u'Improving Berry Crop Production Systems to Meet Current Needs and Challenges in the Mid-Atlantic Region'),
            (u'4742', u'Ecology and Management of Arthropods in Corn'),
            (u'4741', u'Developing Management Strategies for Button Mushroom (Agaricus bisporus) Cultivation to Manage Disease and Improve Yield and to Optimize Cultivation Practices for Specialty Mushrooms, Including Morels (Morchella spp.)'),
            (u'4747', u'Management of Low Maintenance Grass Species for Lawns, Golf Courses, and Sports Turf'),
            (u'8105', u'Leadership &amp; Community Vitality'),
            (u'8101', u'New &amp; Beginning Farmers'),
            (u'8103', u'Business, Entrepreneurship &amp; Economic Development'),
            (u'8102', u'Energy'),
            (u'4608', u'Interactions between Insects and Pathogens/Parasites'),
            (u'4606', u'Insect Ecology and Management in Agroecosystems'),
            (u'4603', u'Supporting Military Families Through Dissemination and Implementation Science'),
            (u'4600', u'Advancing Agronomic Cropping Systems in the Northeast'),
            (u'4685', u'Fuels, Flammability, and Fire Impacts from Changing Landscapes and Invasive Species'),
            (u'4689', u'Improving Soybean Arthropod Pest Management in the U.S.'),
            (u'4619', u'Understanding and Managing Arthropod Pests, Natural Enemies and Pollinators Through Ecologically-Based Integrated Pest Management Approaches On Tree Fruits in Pennsylvania'),
            (u'8401', u'Livestock Profitability &amp; Sustainability'),
            (u'4612', u'Impact Analyses and Decision Strategies for Agricultural Research (NC1034)'),
            (u'4614', u'Impacts of Stress Factors on Performance, Health, and Well-Being of Farm Animals (from W2173)'),
            (u'4616', u'Penn State RREA Program'),
            (u'4693', u'Biological Improvement of Chestnut through Technologies that Address Management of the Species and Its Pathogens and Pests'),
            (u'4694', u'Developing sustainable disease management strategies for tree fruit in Pennsylvania'),
            (u'4697', u'Biomass Properties and Performance'),
            (u'4696', u'Antimicrobial Interventions for Meat and Poultry Products'),
            (u'4698', u'Sustaining Forest\u2019s Health and Vitality Now and in the Future: Working through Landowners, Peers, and Professionals'),
            (u'7070', u'Unknown Project'),
            (u'4596', u'Harnessing Chemical Ecology to Address Agricultural Pest and Pollinator Priorities'),
            (u'4595', u'Ecology and Management of Arthropods in Corn'),
            (u'4598', u'Facilitating Registration of Pest Management Technology for Specialty Crops and Specialty Uses'),
            (u'4599', u'Specialty Crops and Food Systems: Exploring Markets, Supply Chains and Policy Dimensions'),
            (u'8000', u'4-H Youth Development: Base Unit Activity'),
            (u'8001', u'4-H Youth Development: Science'),
            (u'8002', u'4-H Youth Development: Volunteer Management &amp; Development'),
            (u'8003', u'4-H Youth Development: Positive Youth Development'),
            (u'4714', u'Enhancing Poultry Production Systems through Emerging Technologies and Husbandry Practices'),
            (u'4715', u'Environmental Impacts of Equine Operations'),
            (u'4716', u'Sustainable Solutions to Problems Affecting Bee Health'),
            (u'4668', u'Intergenerational Strategies for Promoting Productive Aging, Supporting Families, and Strengthening Communities'),
            (u'4665', u'Improving Livestock Health, Employee Performance, and Protecting Public Health'),
            (u'4666', u'Enhancing Microbial Food Safety by Risk Analysis'),
            (u'4660', u'Improved Integrated Disease Management Based on Science-based, Actionable Information Obtained at Different Scales'),
            (u'4719', u'Laws of Attraction: Evaluating Responses of the Lyme Disease Vector Ixodes Scapularis Nymphs to Tick- and Host-produced Semiochemicals and Their Utility in Surveillance and Control Tools '),
            (u"4662", u"Biology, Epidemiology, and Integrated Management of Cool Season Turfgrass Diseases"),
        ]

        items.sort(key=lambda x:x[1])

        return SimpleVocabulary(
            [SimpleTerm(x[0] ,title=x[1]) for x in items]
        )

ClassificationsVocabularyFactory = ClassificationsVocabulary()
ProjectProgramTeamVocabularyFactory = ProjectProgramTeamVocabulary()
HomeBudgetVocabularyFactory = HomeBudgetVocabulary()
CRMVocabularyFactory = CRMVocabulary()
BOMVocabularyFactory = BOMVocabulary()
CostCenterVocabularyFactory = CostCenterVocabulary()
BudgetVocabularyFactory = BudgetVocabulary()
ProjectVocabularyFactory = ProjectVocabulary()
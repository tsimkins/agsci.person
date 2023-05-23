from zope.i18nmessageid import MessageFactory
personMessageFactory = MessageFactory('agsci.person')

# Register indexers
import agsci.person.indexer

def initialize(context):
    pass

from Products.Five import BrowserView
from zope.interface import implements, Interface

class IPersonView(Interface):
    pass
    
class PersonView(BrowserView):
    pass


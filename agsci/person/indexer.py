from Acquisition import aq_base
from plone.indexer import indexer
from zope.component import provideAdapter

from .content.person import IPerson

# Indexers for person's sortable title
@indexer(IPerson)
def PersonSortableTitle(context):
    t = [getattr(context, x, '') for x in ('last_name', 'first_name')]
    t = [x.lower() for x in t]
    return ", ".join(tuple(t))

provideAdapter(PersonSortableTitle, name='sortable_title')


# Indexers for person's classifications
@indexer(IPerson)
def PersonClassifications(context):
    c = getattr(context, 'classifications', [])

    if c:
        return c

    return []

provideAdapter(PersonClassifications, name='Classifications')


# County for the item
@indexer(IPerson)
def PersonCounty(context):
    return getattr(aq_base(context), 'county', [])

provideAdapter(PersonCounty, name='County')

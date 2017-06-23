from .content.person import IPerson
from plone.indexer import indexer
from zope.component import provideAdapter

# Indexers for person's sortable title
@indexer(IPerson)
def PersonSortableTitle(context):
    t = [getattr(context, x, '') for x in ('last_name', 'first_name')]
    t = map(lambda x: x.lower(), t)
    return tuple(t)

provideAdapter(PersonSortableTitle, name='sortable_title')


# Indexers for person's classifications
@indexer(IPerson)
def PersonClassifications(context):
    c = getattr(context, 'classifications', [])

    if c:
        return c

    return []

provideAdapter(PersonClassifications, name='Classifications')
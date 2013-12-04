"""
purge_orphans.py: instance run script to remove orphaned schemas in
ISchemaSaver utility for all sites in an instance, when applicable.
"""

import transaction

from zope.component.hooks import setSite
from zope.component import queryUtility

from uu.dynamicschema.interfaces import ISchemaSaver


def remove_orphan_schemas(app):
    for site in app.objectValues('Plone Site'):
        setSite(site)
        saver = queryUtility(ISchemaSaver)
        if saver is None:
            continue
        catalog = site.portal_catalog
        query = {
            'portal_type': (
                'uu.formlibrary.definition',
                'uu.qiforms.formseries',
                'uu.formlibrary.fieldgroup'
            ),
        }
        result = catalog.search(query)
        valid_signatures = [
            b._unrestrictedGetObject().signature for b in result
            ]
        orphan_keys = set(saver.keys()).difference(valid_signatures)
        if not orphan_keys:
            continue
        orphan_bytes = sum([len(saver.get(k, '')) for k in orphan_keys])
        print ('[%s] Found %s orphaned schemas (%s bytes); removing.' % (
            site.getId(),
            len(orphan_keys),
            orphan_bytes,
            )
        ),
        for signature in orphan_keys:
            assert signature not in valid_signatures
            del(saver[signature])
            print '.',
        print
        txn = transaction.get()
        txn.note('/'.join(site.getPhysicalPath()))
        txn.note('Removed orphan schemas from ISchemaSaver utility')
        txn.commit()


if __name__ == '__main__' and 'app' in locals():
    remove_orphan_schemas(app)  # noqa

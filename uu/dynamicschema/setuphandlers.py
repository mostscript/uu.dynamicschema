import logging

from zope.component import getSiteManager

from uu.dynamicschema.interfaces import ISchemaSaver
from uu.dynamicschema.schema import SchemaSaver

logger = logging.getLogger('uu.dynamicschema')


def _install_local_utility(context, component, iface, name=u''):
    sm = getSiteManager(context.getSite())
    if sm.queryUtility(iface) is None:
        sm.registerUtility(component, provided=iface, name=name)
        logger.info('Install %s local utility in site.' % iface)


def install_schema_saver(context):
    saver = SchemaSaver()
    _install_local_utility(context, saver, ISchemaSaver)


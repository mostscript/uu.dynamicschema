import unittest2 as unittest

from zope.interface import Interface
from zope import schema


class PkgTest(unittest.TestCase):
    """basic unit tests for package"""
    
    def test_pkg_import(self):
        import uu.dynamicschema  # noqa
        from uu.dynamicschema.zope2 import initialize  # noqa


class IMockWhatever(Interface):
    """Mock interface with a title field"""
    title = schema.TextLine(default=u"Hello testing!")


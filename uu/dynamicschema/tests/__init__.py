import unittest2 as unittest


class PkgTest(unittest.TestCase):
    """basic unit tests for package"""
    
    def test_pkg_import(self):
        import uu.dynamicschema
        from uu.dynamicschema.zope2 import initialize


import doctest
import unittest2 as unittest

from plone.testing import layered

from uu.dynamicschema.tests.layers import DEFAULT_PROFILE_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('../schema.txt'),
                layer=DEFAULT_PROFILE_TESTING),
        ])
    return suite


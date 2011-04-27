import unittest2 as unittest
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import queryUtility, getSiteManager

from uu.dynamicschema.tests.layers import DEFAULT_PROFILE_TESTING
from uu.dynamicschema.interfaces import ISchemaSaver


class DefaultProfileTest(unittest.TestCase):
    """Test default profile's installed configuration settings"""
    
    THEME = 'Sunburst Theme'
    
    layer = DEFAULT_PROFILE_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'f1', title=u'Ex')
        self.content = self.portal['f1']
        self.content.reindexObject()
        self.content_uid = self.content.UID()
    
    def test_installed_schema_saver(self):
        """test locally installed persistent ISchemaSaver utility"""
        saver = queryUtility(ISchemaSaver)
        assert saver is not None
        sm = getSiteManager(self.portal)
        assert saver is sm.queryUtility(ISchemaSaver)


from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting


# fixture layer classes:
class ProductLayer(PloneSandboxLayer):
    """base product layer, for use by per-profile layers"""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """load package zcml to initialize product"""
        import uu.dynamicschema
        self.loadZCML(package=uu.dynamicschema)

    def setUpPloneSite(self, portal):
        """Install named setup profile for class to portal"""
        self.applyProfile(portal, self.PROFILE)


class DefaultProfileTestLayer(ProductLayer):
    """Layer for default profile testing"""

    PROFILE = 'uu.dynamicschema:default'


# fixture bases:
DEFAULT_PROFILE_FIXTURE = DefaultProfileTestLayer()

DEFAULT_PROFILE_TESTING = IntegrationTesting(
    bases=(DEFAULT_PROFILE_FIXTURE,),
    name='uu.dynamicschema:Default Profile')

# Functional testing layers:
DEFAULT_PROFILE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DEFAULT_PROFILE_FIXTURE,),
    name='uu.dynamicschema:Default Profile Functional')


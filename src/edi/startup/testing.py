# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import edi.startup


class EdiStartupLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.startup)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.startup:default')


EDI_STARTUP_FIXTURE = EdiStartupLayer()


EDI_STARTUP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_STARTUP_FIXTURE,),
    name='EdiStartupLayer:IntegrationTesting',
)


EDI_STARTUP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_STARTUP_FIXTURE,),
    name='EdiStartupLayer:FunctionalTesting',
)


EDI_STARTUP_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_STARTUP_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiStartupLayer:AcceptanceTesting',
)

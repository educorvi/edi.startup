# -*- coding: utf-8 -*-
from edi.startup.content.position import IPosition  # NOQA E501
from edi.startup.testing import EDI_STARTUP_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class PositionIntegrationTest(unittest.TestCase):

    layer = EDI_STARTUP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Invoice',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_position_schema(self):
        fti = queryUtility(IDexterityFTI, name='Position')
        schema = fti.lookupSchema()
        self.assertEqual(IPosition, schema)

    def test_ct_position_fti(self):
        fti = queryUtility(IDexterityFTI, name='Position')
        self.assertTrue(fti)

    def test_ct_position_factory(self):
        fti = queryUtility(IDexterityFTI, name='Position')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPosition.providedBy(obj),
            u'IPosition not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_position_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Position',
            id='position',
        )

        self.assertTrue(
            IPosition.providedBy(obj),
            u'IPosition not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('position', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('position', parent.objectIds())

    def test_ct_position_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Position')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

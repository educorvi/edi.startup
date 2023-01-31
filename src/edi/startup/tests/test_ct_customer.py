# -*- coding: utf-8 -*-
from edi.startup.content.customer import ICustomer  # NOQA E501
from edi.startup.testing import EDI_STARTUP_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class CustomerIntegrationTest(unittest.TestCase):

    layer = EDI_STARTUP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_customer_schema(self):
        fti = queryUtility(IDexterityFTI, name='Customer')
        schema = fti.lookupSchema()
        self.assertEqual(ICustomer, schema)

    def test_ct_customer_fti(self):
        fti = queryUtility(IDexterityFTI, name='Customer')
        self.assertTrue(fti)

    def test_ct_customer_factory(self):
        fti = queryUtility(IDexterityFTI, name='Customer')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICustomer.providedBy(obj),
            u'ICustomer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_customer_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Customer',
            id='customer',
        )

        self.assertTrue(
            ICustomer.providedBy(obj),
            u'ICustomer not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('customer', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('customer', parent.objectIds())

    def test_ct_customer_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Customer')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_customer_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Customer')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'customer_id',
            title='Customer container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )

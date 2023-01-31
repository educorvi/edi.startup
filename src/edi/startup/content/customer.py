# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from edi.startup import _

class ICustomer(model.Schema):
    """ Marker interface and Dexterity Python Schema for Customer
    """
    
    customer_number = schema.TextLine(title=_('Customer Number'), required=False)
 
    contact_person = schema.TextLine(title=_('Contact Person'), required=False)

    contact_email = schema.TextLine(title=_('Contact E-Mail'))

    contact_phone = schema.TextLine(title=_('Contact Phone'), required=False)

    contact_mobile = schema.TextLine(title=_('Contact Mobil'), required=False)

    street = schema.TextLine(title=_('Street and Number'))

    zipcode = schema.TextLine(title=_('Zip-Code'))

    city = schema.TextLine(title=_('City'))


@implementer(ICustomer)
class Customer(Container):
    """ Content-type class for ICustomer
    """

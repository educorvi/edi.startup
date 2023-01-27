# -*- coding: utf-8 -*-
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import implementer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice


from edi.startup import _


class IInvoice(model.Schema):
    """ Marker interface and Dexterity Python Schema for Invoice
    """

    invoice_nr = schema.TextLine(title=_("Invoice Number"),
            description=_("This number will be created automatically after publishing"),
            required=False)

    customer = RelationChoice(title=_("Customer-Reference"),
            description=_("Choose a Customer they will get the invoice"),
            vocabulary='plone.app.vocabularies.Catalog',
            required=True)

    directives.widget(
        'customer',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ["Customer"],
            'basePath': make_relation_root_path,
        },
    )

    project = RelationChoice(title=_("Project-Reference"),
            description=_("For which project you want to create an invoice?"),
            vocabulary='plone.app.vocabularies.Catalog',
            required=True)

    directives.widget(
        'project',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ["Folder"],
            'basePath': make_relation_root_path,
        },
    )
    
    term_of_payment = schema.TextLine(title=_("Term of Payment"),
            description=_("A sentence to describe the term of payment"),
            default=_("Within 14 days without discount."),
            required=True)


    discount = schema.Int(title=_("Discount in percent"),
            required=False)

    cashdiscount = schema.TextLine(title=_("Cash-Discount Comment"),
            description=_("Describe the condition to allow a cash-discount"),
            required=False)


@implementer(IInvoice)
class Invoice(Container):
    """ Content-type class for IInvoice
    """

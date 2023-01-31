from plone import schema
from plone.supermodel.directives import fieldset
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from zope.interface import Interface
from edi.startup import _
from plone.z3cform import layout
from z3c.form import form


class IStartupSettings(Interface):

    company_name = schema.TextLine(title=_("Company Name"))

    company_street_number = schema.TextLine(title=_("Company Street and Number"))

    company_zipcode = schema.TextLine(title=_("Company ZIP Code"))

    company_city = schema.TextLine(title=_("Company City"))

    company_contact = schema.TextLine(title=_("Contact Person for Invoices"))

    company_contact_email = schema.TextLine(title=_("Contact E-Mail for Questions about Invoices"))

    company_contact_phone = schema.TextLine(title=_("Contact Phone for Questions about Invoices"), required=False)

    fieldset(
        'bank',
        label=_("Bank Account"),
        fields=('bank', 'bankaccount', 'bic'),
    )

    bank = schema.TextLine(title=_("Name of the Bank"))

    bankaccount = schema.TextLine(title=_("IBAN-Number of Bank-Account"))

    bic = schema.TextLine(title=_("BIC Bank Identifier Code"), required=False)

    fieldset(
        'invoice',
        label=_("Invoice Preferences"),
        fields=('invoice_format', 'first_number', 'register_type', 'register_number', 'jurisdiction', 'tax_number', 'vat_number', 'tax_rate')
    )

    invoice_format = schema.TextLine(title=_("Format for Invoice Numbers"),
                                     description=_("Use the fstring Format with variables {year}, {seq-number}, look at default as example."),
                                     default="{year}-{seq-number}")
    
    first_number = schema.Int(title=_("First Invoice Number per Year"),
                              default=10000)

    register_type = schema.TextLine(title=_("Type of Business Register"), required=False)

    register_number = schema.TextLine(title=_("Register Number"), required=False)

    jurisdiction = schema.TextLine(title=_("Place of jurisdiction"), required=False)

    tax_number = schema.TextLine(title=_("TAX-Number"))

    vat_number = schema.TextLine(title=_("VAT-Number"))

    tax_rate = schema.Int(title=_("Tax rate in percent"))
    
    fieldset(
        'rates',
        label=_("Service Rates"),
        fields=('practice', 'trainee', 'professional', 'expert')
    )

    practice = schema.Float(title=_("Rate per hour for temporary staff or pupils"))

    trainee = schema.Float(title=_("Rate per hour for trainess oder students"))

    professional = schema.Float(title=_("Rate per hour for professionals"))

    expert = schema.Float(title=_("Rate per hour for experts"))

class StartupSettingsEditForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IStartupSettings

StartupControlPanelView = layout.wrap_form(StartupSettingsEditForm, ControlPanelFormWrapper)
StartupControlPanelView.label = u"Settings for edi.startup"

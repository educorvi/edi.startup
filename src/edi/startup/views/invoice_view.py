# -*- coding: utf-8 -*-
from edi.startup import _
from Products.Five.browser import BrowserView
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class InvoiceView(BrowserView):

    def __call__(self):
        self.customerobj = vars(self.context.customer.to_object)
        self.date = self.context.effective().strftime('%d.%m.%Y')
        self.preferences = self.get_preferences()
        self.positions = self.get_positions()
        self.summary = self.get_summary()
        print(self.summary)
        return self.index()

    def get_preferences(self):
        address = {}
        address['company_name'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_name')
        address['company_street_number'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_street_number') 
        address['company_zipcode'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_zipcode') 
        address['company_city'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_city') 
        address['company_contact'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_contact') 
        address['company_contact_email'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_contact_email') 
        address['company_contact_phone'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.company_contact_phone')
        address['company_bank'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.bank') 
        address['company_bankaccount'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.bankaccount')
        address['company_bic'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.bic') 
        address['invoice_format'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.invoice_format')
        address['first_number'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.first_number')
        address['register_type'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.register_type')
        address['register_number'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.register_number')
        address['jurisdiction'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.jurisdiction')
        address['tax_number'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.tax_number') 
        address['vat_number'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.vat_number') 
        address['tax_rate'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.tax_rate')
        address['practice'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.practice')
        address['trainee'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.trainee')
        address['professional'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.professional')
        address['expert'] = api.portal.get_registry_record('edi.startup.browser.panelsettings.IStartupSettings.expert')
        return address

    def get_positions(self):
        raw_positions = self.context.getFolderContents()
        positions = []
        for pos in raw_positions:
            position = {}
            posobj = pos.getObject()
            amount = sum((self.preferences['practice'] * posobj.hours_practice,
                          self.preferences['trainee'] * posobj.hours_trainee,
                          self.preferences['professional'] * posobj.hours_professional,
                          self.preferences['expert'] * posobj.hours_expert))
            amount = round(amount, 2)
            formatted_amount = "%0.2f" % (amount,)
            hours = sum((posobj.hours_practice, posobj.hours_trainee, posobj.hours_professional, posobj.hours_expert))
            position['title'] = posobj.title
            position['url'] = posobj.absolute_url()
            position['posnr'] = len(positions) + 1
            position['description'] = posobj.description
            position['start'] = posobj.start.strftime('%d.%m.%Y')
            position['end'] = posobj.end.strftime('%d.%m.%Y')
            position['practice'] = posobj.hours_practice
            position['trainee'] = posobj.hours_trainee
            position['professional'] = posobj.hours_professional
            position['expert'] = posobj.hours_expert
            position['amount'] = amount
            position['formatted_amount'] = formatted_amount
            position['hours'] = hours
            positions.append(position)
        return positions

    def get_summary(self):
        before_tax = sum([position['amount'] for position in self.positions])
        tax_rate = self.preferences.get('tax_rate')
        after_tax = (before_tax * (100 + tax_rate)) / 100
        after_tax = round(after_tax, 2)
        tax_diff = round((after_tax - before_tax), 2)
        return (before_tax, tax_diff, after_tax)

class PureInvoiceView(InvoiceView):
    """ Pure View without Boilerplate or Plonesite for Printing """

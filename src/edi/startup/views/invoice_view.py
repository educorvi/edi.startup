# -*- coding: utf-8 -*-

from edi.startup import _
from Products.Five.browser import BrowserView

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class InvoiceView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('invoice_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.msg = _(u'A small message')
        self.customerobj = vars(self.context.customer.to_object)
        self.date = self.context.effective().strftime('%d.%m.%Y')
        return self.index()

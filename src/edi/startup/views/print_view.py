import tempfile
from edi.startup.views.invoice_view import InvoiceView
from edi.startup.pdf.createpdf import createpdf

class PrintView(InvoiceView):

    def __call__(self):
        self.customerobj = vars(self.context.customer.to_object)
        self.date = self.context.effective().strftime('%d.%m.%Y')
        self.preferences = self.get_preferences()
        self.positions = self.get_positions()
        self.summary = self.get_summary()
        
        filehandle = tempfile.TemporaryFile()
        createpdf(filehandle, self)
        filehandle.seek(0)
        Response = self.request.response
        Response.setHeader("content-type", "application/pdf")
        Response.setHeader("content-disposition", "attachment; filename=%s.pdf" % self.context.id)
        return filehandle.read()

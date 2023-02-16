import os.path
import tempfile
from datetime import date
from time import localtime, gmtime, strftime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import grey, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus import Table
from reportlab.platypus.flowables import Flowable, Spacer, Image, PageBreak, BalancedColumns
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT as _r
from reportlab.lib.enums import TA_CENTER as _c
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from apply import apply

from edi.startup import _

edinormal = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Cambay-Regular.ttf')
edibold = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Cambay-Bold.ttf')

pdfmetrics.registerFont(TTFont('EDINormal', edinormal))
pdfmetrics.registerFont(TTFont('EDIBold', edibold))



class PdfBaseTemplate(BaseDocTemplate):
    """Basistemplate for PDF-Prints"""

    def __init__(self, filename, **kw):
        frame1 = Frame(1 * cm, 3 * cm, 18.5 * cm, 25 * cm, id='F1', showBoundary=False)
        self.allowSplitting = 0
        apply(BaseDocTemplate.__init__, (self, filename), kw)
        self.addPageTemplates(PageTemplate('normal', [frame1]))

class NumberedCanvas(canvas.Canvas):
    """Add Page number to generated PDF"""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("EDIBold", 7.5)
        if self._pageNumber < page_count:
            self.drawRightString(19.3 * cm, 1 * cm, "Seite %d von %d" % (self._pageNumber, page_count))
        if self._pageNumber == page_count:
            self.drawString(1.2 * cm, 2.4 * cm, "educrovi GmbH & Co. KG")
            self.drawString(1.2 * cm, 2 * cm, "Karolinenstraße 17")
            self.drawString(1.2 * cm, 1.6 * cm, "90763 Fürth")
            self.drawString(1.2 * cm, 1.2 * cm, "www.educorvi.de")
            self.drawString(9.25 * cm, 2.4 * cm, "Raiffeisenbank")
            self.drawString(9.25 * cm, 2 * cm, "Bad Windsheim")
            self.drawString(9.25 * cm, 1.6 * cm, "IBAN: DE96 7606 9372 0000 086010")
            self.drawString(9.25 * cm, 1.2 * cm, "BIC: GENODEF1WDS")
            self.drawRightString(19.3 * cm, 2.4 * cm, "Seite %d von %d" % (self._pageNumber, page_count))
            self.drawString(16.5 * cm, 2.0 * cm, "Handelsregister: HRA10594")
            self.drawString(16.5 * cm, 1.6 * cm, "Amtsgericht & Finanzamt Fürth")
            self.drawString(16.5 * cm, 1.2 * cm, "Steuernummer: 218/157/05901")



def createpdf(filehandle, content):
    """Funktion zum Schreiben der PDF-Datei"""

    story = []  # Alle Elemente des PDFs werden der Story hinzugefuegt

    # Styles fuer normale Paragraphen, gelesen aus dem SampleStyleSheet
    stylesheet = getSampleStyleSheet()

    h1 = stylesheet['Heading1']
    h1.fontname = 'EDIBold'

    h2 = stylesheet['Heading2']
    h2.fontName = 'EDIBold'

    h3 = stylesheet['Heading3']
    h3.fontname = 'EDIBold'

    code = stylesheet['Code']

    bodytext = stylesheet['BodyText']
    bodytext.fontName = 'EDINormal'

    bodybold = stylesheet['BodyText']
    bodybold.fontName = 'EDIBold'

    # Weitere Styles fuer Paragraphen
    stylesheet.add(ParagraphStyle(name='smallbody', fontName='EDINormal', fontSize=9, spaceAfter=5))
    stylesheet.add(ParagraphStyle(name='normal', fontName='EDINormal', fontSize=7.5, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name='free', fontName='EDINormal', fontSize=7.5, borderPadding=0))
    stylesheet.add(ParagraphStyle(name='right', fontName='EDINormal', fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_r))
    stylesheet.add(ParagraphStyle(name='center', fontName='EDINormal', fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_c))
    stylesheet.add(ParagraphStyle(name='bold', fontName='EDIBold', fontSize=7.5, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name='boldnew', fontName='EDIBold', fontSize=9, borderPadding=(5, 3, 3, 5)))
    stylesheet.add(ParagraphStyle(name='boldright', fontName='EDIBold', fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_r))
    stylesheet.add(ParagraphStyle(name='boldcenter', fontName='EDIBold', fontSize=7.5, borderPadding=(5, 3, 3, 5), alignment=_c))

    smallbody = stylesheet['smallbody']
    bullet = stylesheet['Bullet']
    bullet.fontSize=9
    bullet.fontName='EDINormal'
    entry_normal = stylesheet['normal']
    entry_free = stylesheet['free']
    entry_right = stylesheet['right']
    entry_center = stylesheet['center']
    entry_bold = stylesheet['bold']
    entry_boldnew = stylesheet['boldnew']
    entry_boldright = stylesheet['boldright']
    entry_boldcenter = stylesheet['boldcenter']

    im = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/educorvi_280.jpg')
    logo = Image(im)
    logo.drawHeight = 6 * cm * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 6 * cm
    logo.hAlign = 'RIGHT'

    # Datum
    datum = u"Datum: %s" % (strftime("%d.%m.%Y"))
    zeit = u"Zeit: %s" % (strftime("%H:%M:%S", localtime()))

    colWidths = [9.5*cm, 2.75*cm, 6.25*cm]
    formtitle = _("Invoice")
    testheadline = u'<font color="#008c8e"><b>%s</b></font>' % formtitle
    toptable = [[Paragraph(testheadline, h2), Paragraph(u" ", bodytext), logo]]
    table = Table(toptable, colWidths=colWidths, style=[('VALIGN', (0, 0), (-1, -1), 'TOP')])
    table.hAlign = 'CENTER'
    story.append(table)
    story.append(Spacer(0 * cm, 0.5 * cm))

    dummyobj = "12345"
    customer_number = _("Customer number") + ": " + content.customerobj['customer_number']
    invoice_number = _("Invoice number") + ": " + dummyobj
    date = _("Date") + ": " + content.date

    colWidths = [13 * cm, 10 * cm, 10 * cm]
    lastline = str(content.customerobj['zipcode']) + ' ' + str(content.customerobj['city'])
    receiver = [[Paragraph(content.customerobj['title']), Paragraph(customer_number)],
                [Paragraph(content.customerobj['contact_person']), Paragraph(invoice_number)],
                [Paragraph(content.customerobj['street']), Paragraph(date)], [Paragraph(lastline)]]
    table2 = Table(receiver, colWidths=colWidths)
    table2.hAlign = 'LEFT'
    story.append(table2)

# Invoice details in separate row
    """
    story.append(Spacer(0 * cm, 2 * cm))
    colWidths = [10 * cm, 10 * cm, 10 * cm]
    dummyobj = "12345"
    customer_number = _("Customer number") + ": " + content.customerobj['customer_number']
    invoice_number = _("Invoice number") + ": " + dummyobj
    date = _("Date") + ": " + content.date

    invoicedetails = [[Paragraph(customer_number)], [Paragraph(invoice_number)],
                [Paragraph(date)]]
    invoicedetailstable = Table(invoicedetails, colWidths=colWidths)
    invoicedetailstable.hAlign = 'LEFT'
    story.append(invoicedetailstable)
    """

    colWidths = [1*cm, 8*cm, 4*cm, 4*cm]
    services = _("Services")
    hours = _("Hours")
    subtotal = _("Subtotal")
    data = """\
Indexierung aller relvanten Daten aus den Objekten der Projektsteuerung<br/>
Period: 14.12.2022 - 25.01.2023<br/>
<br/>
<b>Employee Qualifications:</b><br/>
Professional: 12 Hours
"""
    story.append(Spacer(0 * cm, 2 * cm))
    datatable = [
                 [Paragraph("#"), Paragraph(services, entry_normal), Paragraph(hours, entry_normal), Paragraph(subtotal, entry_normal)],
                 [Paragraph("1"), Paragraph(data, entry_normal), Paragraph("12", entry_normal), Paragraph("1200,00 €", entry_right)]
                ]
    table = Table(datatable, colWidths=colWidths)
    story.append(table)

    story.append(Spacer(0 * cm, 2 * cm))

    datanew = content.positions
    datatable2 = list()
    datatable2.append([Paragraph("#"), Paragraph(services, entry_normal), Paragraph(hours, entry_normal), Paragraph(subtotal, entry_normal)])
    for pos in datanew:
        qualis = list()
        if pos['practice']:
            qualis.append(_('Practice') + ': ' + str(pos['practice']))
        if pos['trainee']:
            qualis.append(_('Trainee') + ': ' + str(pos['trainee']))
        if pos['professional']:
            qualis.append(_('Professional') + ': ' + str(pos['professional']))
        if pos['expert']:
            qualis.append(_('Expert') +': ' + str(pos['expert']))

        summedhours = pos['practice'] + pos['trainee'] + pos['professional'] + pos['expert']
        subtotalrow = (pos['practice'] * content.preferences['practice']) + \
                      (pos['trainee'] * content.preferences['trainee']) + \
                      (pos['professional'] * content.preferences['professional']) + \
                      (pos['expert'] * content.preferences['expert'])

        rowdata = pos['title'] + '<br/>' + _("Period") + ": " + pos['start'] + " - " + pos['end'] + '<br/><br/>' + _('Employee Qualifications') + ':'
        for quali in qualis:
            rowdata = rowdata + '<br/>' + quali
        row = [Paragraph(str(pos['posnr'])), Paragraph(str(rowdata)), Paragraph(str(summedhours)), Paragraph(str(subtotalrow))]
        datatable2.append(row)
    table = Table(datatable2, colWidths=colWidths)
    story.append(table)

    story.append(Spacer(0 * cm, 2 * cm))
    summarytable = list()
    taxratestring = _("Tax rate ") + str(content.preferences['tax_rate']) + '%'
    summarydata = content.summary
    summarytable.append([Paragraph(_("Subtotal")), Paragraph(str(summarydata[0]))])
    summarytable.append([Paragraph(taxratestring), Paragraph(str(summarydata[1]))])
    summarytable.append([Paragraph(_("Total")), Paragraph(str(summarydata[2]))])
    colWidths = [13 * cm, 4 * cm]
    table = Table(summarytable, colWidths=colWidths)
    story.append(table)

    doc = PdfBaseTemplate(filehandle, pagesize=A4, leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=1.5*cm,bottomMargin=-10*cm)
    doc.build(story, canvasmaker=NumberedCanvas)

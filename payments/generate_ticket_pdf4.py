import io, os
from reportlab.pdfgen import canvas
import qrcode
from reportlab.lib.pagesizes import letter, A5, landscape
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing
from datetime import timedelta, datetime
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet

#----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)
#----------generate unique code for email subscription conf--------------------
def ticket_nr(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

def generate_ticket(data):
    doc = SimpleDocTemplate(data['file'], pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["Normal"]

    qr_code = QrCodeWidget(data['ticketseries'])
    bounds = qr_code.getBounds()

    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]

    d = Drawing(2 * qr_width, 2 * qr_height)
    d.add(qr_code)

    elements = []

    elements.append(Paragraph("Visitor Ticket", title_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Visitor Name: {data['first_name']} {data['last_name']}", body_style))
    elements.append(Spacer(1, 6))

    elements.append(d)

    doc.build(elements)
def generate_pdf_ticket(data):
    x=200
    y=90
    buffer=io.BytesIO()
    
    pagesize = (210*mm, 90*mm)
    # ticket=canvas.Canvas(data['file'],pagesize=pagesize)
    ticket = BaseDocTemplate(data['file'], showBoundary=1, pagesize=pagesize, leftMargin=15 * mm,
                                    rightMargin=15 * mm,
                                    topMargin=20 * mm,
                                    bottomMargin=15 * mm)
    ticket.pagesize = landscape(pagesize)
    paragraphs = PageTemplate(id='firstpage',frames=[leftlogoframe,TopCenter,rightlogoframe,frame1,frame2],onPage=foot1)

    paragraphs = []
    styles = getSampleStyleSheet()
    barcode=code39.Extended39(data['ticketseries'],barWidth=0.5*mm,barHeight=20*mm)
    text = "This is some sample text."

    
    # try:
    #     ticket.drawImage(r'payments/ticket_logos/ticket_bg.png', x=0, y=0,width=200, preserveAspectRatio=True, mask='auto')
    #     #add park logo
    #     ticket.drawImage(r'payments/ticket_logos/bucegi2.png', x=175, y=4,width=22)
    #     #add company title
    #     ticket.drawString(145,10, r"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.")
    #     #add romsilva logo
    #     ticket.drawImage(r'payments/ticket_logos/rnp-romsilva3.png', x=5, y=5,width=22)
    #     # add buyer
    #     ticket.drawString(10,30, f"Cumparator: {data['first_name'].title()} {data['last_name'].title()}")
    #     # add expiry date
    #     ticket.drawString(10,40,"Data expirarii: {}".format(data['date']))
    # except Exception as e:
    #     print(e)
    # ticket.showPage()
    # try:
    #     ticket.save()
    # except Exception as e:
    #     print(e)
    pdf=buffer.getvalue()
    # buffer.close() 
    paragraphs.append(Image(r'ticket_logos/ticket_bg.png', width=190, height=70))
    paragraphs.append(Image(r'ticket_logos/bucegi2.png', width=22, height=19))
    paragraphs.append(Paragraph(r"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.", styles["Normal"]))
    paragraphs.append(Image(r'ticket_logos/rnp-romsilva3.png', width=22, height=21))
    paragraphs.append(Image(gen_qr(data['file']), width=30,height=30))
    ticket.watermark = 'BUCEGI'

    ticket.build(paragraphs)
    return ticket

# def someView(request):
#  EmailMsg=mail.EmailMessage(YourSubject,YourEmailBodyCopy,'email@email.com',["email@email.com"],headers={'Reply-To':'email@email.com'})
#  pdf=createPDF(request)
#  EmailMsg.attach('yourChoosenFileName.pdf',pdf,'application/pdf')
#  EmailMsg.send()
if __name__ == "__main__":
    y = 3
    x = 6
    series='DBPNO000001'
    file_nr = f"{series}-{ticket_series()}"
    data = {
                        "first_name":'daniel',
                        "last_name":'ungureanu',
                        "file":'ticket-{}.pdf'.format(file_nr),
                        "series":'https://bucegipark.ro',
                        "amount": 10,
                        "date": datetime.today().date() + timedelta(days=90),
                        "ticketseries": "Serie tichet",
                    }
    generate_ticket(data)
from reportlab.lib.pagesizes import letter
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.barcode.qr import QrCodeWidget
from datetime import timedelta, datetime
from reportlab.graphics.shapes import Drawing

#----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)

class CenteredImage(Image):
    def wrap(self, width, height):
        self.width = width
        self.height = height
        return width, height

def generate_qr_code(data):
    qr_code = QrCodeWidget(data)
    bounds = qr_code.getBounds()

    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]

    d = Drawing(25, 25, transform=[25. / qr_width,0,0,25. / qr_height,0,0])
    d.add(qr_code)
    return d

def generate_ticket(data):
    buffer=io.BytesIO()
    
    pagesize = (210*mm, 90*mm)
    doc = SimpleDocTemplate(data['file'], pagesize=pagesize)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["Normal"]

    left_logo = r'ticket_logos/bucegi2.png'  # Path to your left logo image
    right_logo = r'ticket_logos/rnp-romsilva3.png'  # Path to your right logo image
    background_image = r'ticket_logos/ticket_bg.png'  # Path to your background image

    left_logo_img = Image(left_logo, width=20*mm, height=20*mm)
    right_logo_img = Image(right_logo, width=20*mm, height=20*mm)
    background_img = Image(background_image, width=200*mm, height=80*mm)
    qr_code_img = Image(generate_qr_code(data), width=25*mm, height=25*mm)
    elements = []

    # Add background image
    elements.append(background_img)

    # Add left logo
    left_logo_img.wrapOn(doc, 20*mm, 20*mm)
    left_logo_img.drawOn(doc, 0, 80*mm - 20*mm)

    # Add right logo
    right_logo_img.wrapOn(doc, 20*mm, 20*mm)
    right_logo_img.drawOn(doc, 200*mm - 20*mm, 80*mm - 20*mm)

    # Add QR code
    qr_code_img.wrapOn(doc, 25*mm, 25*mm)
    qr_code_img.drawOn(doc, 200*mm - 25*mm, 0)

    # Build the PDF document
    doc.build(elements)
    return ticket

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
from django.http import FileResponse
import io
import qrcode
import random, string
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, PCMYKColor
from reportlab.lib import utils
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter, A5
from reportlab.lib.units import mm
from datetime import timedelta, datetime

from django.utils.translation import gettext_lazy as _

 #----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)
#----------generate unique code for email subscription conf--------------------
def ticket_nr(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

def save_pdf_to_location(pdf_data, file_path):
    """
    Save the PDF data to a physical location on the hard drive.
    
    Args:
        pdf_data: Binary data of the PDF.
        file_path: Path where the PDF should be saved.
        
    Returns:
        True if the PDF was successfully saved, False otherwise.
    """
    try:
        with open(file_path, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        return True
    except Exception as e:
        print(f"Error saving PDF to {file_path}: {e}")
        return False
    
def generate_pdf_ticket(data):
    """
        Save the PDF data to a physical location on the hard drive.
        
        Args:
            pdf_data: Binary data of the PDF.
            file_path: Path where the PDF should be saved.
            
        Returns:
            True if the PDF was successfully saved, False otherwise.
    """
    from io import BytesIO
    """
    Generate a PDF ticket with background image and other dynamic content.

    Args:
        data (dict): Dictionary containing ticket data.
        background_image_path (str): Path to the background image file.

    Returns:
        bytes: Binary data of the generated PDF.
    """
    from io import BytesIO
    
    # Constants
    PAGE_WIDTH = 200 * mm
    PAGE_HEIGHT = 90 * mm
    COVER_WIDTH = PAGE_WIDTH * 0.3

    buffer = BytesIO()
    pagesize = (PAGE_WIDTH, PAGE_HEIGHT)

    ticket=canvas.Canvas(buffer,pagesize=pagesize)
    try:
        # Draw black border around the entire ticket
        ticket.setStrokeColor(Color(0,0,0))
        ticket.rect(0, 0, PAGE_WIDTH+2, PAGE_HEIGHT+2)
        # Draw background image
        ticket.drawImage(data['background_image_path'], x=0, y=0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
        
        # Add Bucegi logo to the upper-left corner
        ticket.drawImage(data['bucegi_logo'], x=10, y=PAGE_HEIGHT - 68, width=62, height=59, mask='auto')

        # Add RNP logo to the upper-right corner
        ticket.drawImage(data['rnp_logo'], x=PAGE_WIDTH - 250, y=PAGE_HEIGHT - 70, width=62, height=61, mask='auto')

        # Add company name and center it
        company_name_width = ticket.stringWidth(data['company_name'], "Helvetica-Bold", 14)
        unit_name_width = ticket.stringWidth(data['unit_name'], "Helvetica-Bold", 10)
        title_width = ticket.stringWidth(data['title'], "Helvetica-Bold", 30)

        company_name_x = (PAGE_WIDTH * 0.7 - company_name_width) / 2
        unit_name_x = (PAGE_WIDTH * 0.7 - unit_name_width) / 2
        title = (PAGE_WIDTH * 0.7 - title_width) / 2

        ticket.setFont("Helvetica-Bold", 14)
        ticket.drawString(company_name_x, PAGE_HEIGHT - 30, data['company_name'])
        ticket.setFont("Helvetica-Bold", 10)
        ticket.drawString(unit_name_x, PAGE_HEIGHT - 50, data['unit_name'])
        ticket.setFont("Helvetica-Bold", 30)
        ticket.drawString(title, PAGE_HEIGHT -100, data['title'])

       # Add buyer info box on the right side
        ticket.setFillColor(Color(0, 0, 0, alpha=0.5))  # Light gray color
        ticket.setStrokeColor(Color(0, 0, 0))  # Black color
        ticket.rect(PAGE_WIDTH - COVER_WIDTH, 0, COVER_WIDTH, PAGE_HEIGHT+9, fill=1)  # Draw and fill rectangle
        #set box color
        ticket.setFillColor(Color(1, 1, 1))  # white color
        ticket.setStrokeColor(Color(0, 0, 0))  # Black color
        # draw boxes
        ticket.rect(PAGE_WIDTH - COVER_WIDTH+6, PAGE_HEIGHT - 80, PAGE_WIDTH - 410, 20, fill=1)  # Draw rectangle
        ticket.rect(PAGE_WIDTH - COVER_WIDTH+6, PAGE_HEIGHT - 120, PAGE_WIDTH - 410, 20, fill=1)  # Draw rectangle
        # set text font
        ticket.setFont("Helvetica", 10)
        # set text color
        ticket.setFillColor(Color(0, 0, 0))  # Black color
        # add buyer name in a box
        ticket.drawString(PAGE_WIDTH - COVER_WIDTH+8, PAGE_HEIGHT - 74, f"Cumparator: {data['first_name'].title()} {data['last_name'].title()}")
        # Add expiry date in a box
        ticket.drawString(PAGE_WIDTH - COVER_WIDTH+8, PAGE_HEIGHT - 114, f"Data expirarii: {data['validity']}")

        # Add QR code directly to PDF
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data['qr'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert QR code image to BytesIO
        qr_byte_io = BytesIO()
        qr_img.save(qr_byte_io, format='PNG')
        qr_byte_io.seek(0)

        # Calculate the correct height based on the aspect ratio
        qr_img_width, qr_img_height = qr_img.size
        aspect_ratio = qr_img_width / qr_img_height
        qr_height = COVER_WIDTH / aspect_ratio-30
        qr_width = COVER_WIDTH / aspect_ratio-30


        # Draw QR code onto the PDF using drawImage
        ticket.drawImage(utils.ImageReader(qr_byte_io), PAGE_WIDTH - 430, 5, width=qr_width, height=qr_height)

        # Add webpage address at the bottom
        ticket.setFillColor(Color(1,1,1))  # white color
        website_width = ticket.stringWidth("www.bucegipark.ro", "Helvetica-Bold", 14)

        website_x = (PAGE_WIDTH - COVER_WIDTH+455) / 2

        ticket.setFont("Helvetica-Bold", 12)
        ticket.drawString(website_x, 5, "www.bucegipark.ro")

    except Exception as e:
        print(f"Error generating PDF ticket: {e}")
    #finish page
    ticket.showPage()
    ticket.save()
    pdf=buffer.getvalue()
    buffer.close()
    return pdf

if __name__ == "__main__":
    y = 3
    x = 6
    series='DBPNO000001'
    file_nr = f"{series}{ticket_series()}"
    data = {            
                        "qr":"sadadasdada13",
                        "first_name":'daniel',
                        "last_name":'ungureanu',
                        "file":'ticket-{}.pdf'.format(file_nr),
                        "series":series,
                        "amount": 1,#in production need to divide by 10
                        "validity": datetime.today().date() + timedelta(days=90),
                        'title':"TICHET DE VIZITATOR",
                        'background_image_path':r"ticket_logos/ticket_bg.png",
                        "bucegi_logo": r'ticket_logos/bucegi2.png',
                        "rnp_logo": r'ticket_logos/rnp-romsilva3.png',
                        "company_name":r'RNP ROMSILVA',
                        "unit_name":r'ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.',

                    }
    pdf= generate_pdf_ticket(data)
    save_pdf_to_location(pdf,"tickets/{}".format(data['file']))
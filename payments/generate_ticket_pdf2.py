import os
import qrcode
from pathlib import Path
import random, string
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib import utils
import qrcode
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from qrcode.constants import ERROR_CORRECT_L
from reportlab.lib.units import mm
from datetime import timedelta, datetime

from django.utils.translation import gettext_lazy as _

SCRIPT_DIR = Path(__file__).parent.absolute()
# --- REGISTER TRUETYPE FONTS FOR DIACRITICS ---
FONT_DIR = SCRIPT_DIR.parent / 'static' / 'fonts'

try:
    pdfmetrics.registerFont(TTFont('DejaVu', str(FONT_DIR / 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))
except Exception as e:
    print(f"Warning: Could not load custom TTF fonts. Falling back or check path: {e}")
 #----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)
#----------generate unique code for email subscription conf--------------------
def ticket_nr(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

def save_pdf_to_location(pdf_data, file_path):
    """
    Generates a PDF ticket.
    Args:
        pdf_data: Binary data of the PDF.
        file_path: Path where the PDF should be saved (not used in production to save space).
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
    Generates PDF ticket.

    Args:
        data (dict): Dictionary containing ticket data.

    Returns:
        bytes: Binary data of the generated PDF, or None if failed.
    """
    from io import BytesIO
    
    # Dimensions (200mm x 90mm standard ticket size)
    PAGE_WIDTH = 200 * mm
    PAGE_HEIGHT = 90 * mm
    STUB_WIDTH = PAGE_WIDTH * 0.32  # 32% width for the right-hand info panel

    buffer = BytesIO()
    pagesize = (PAGE_WIDTH, PAGE_HEIGHT)
    ticket = canvas.Canvas(buffer, pagesize=pagesize)
    
    try:
        # 1. Base Canvas Background (Clean White)
        ticket.setFillColor(Color(1, 1, 1))
        ticket.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        if os.path.exists(data.get('background_image_path', '')):
            ticket.saveState()
            ticket.setFillAlpha(0.15)
            ticket.drawImage(data['background_image_path'], x=0, y=0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
            ticket.restoreState()

        # 2. Outer Border & Frame
        ticket.setStrokeColor(Color(0.15, 0.3, 0.18))
        ticket.setLineWidth(1.5)
        ticket.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT)

        # 3. Logos
        if os.path.exists(data.get('bucegi_logo', '')):
            ticket.drawImage(data['bucegi_logo'], x=10, y=PAGE_HEIGHT - 58, width=45, height=42, mask='auto')
        if os.path.exists(data.get('rnp_logo', '')):
            ticket.drawImage(data['rnp_logo'], x=PAGE_WIDTH - STUB_WIDTH - 55, y=PAGE_HEIGHT - 58, width=45, height=45, mask='auto')

        # 4. Header Text (Main Left Section)
        main_section_width = PAGE_WIDTH - STUB_WIDTH
        
        ticket.setFillColor(Color(0.1, 0.2, 0.12))
        ticket.setFont("DejaVu-Bold", 11)
        company_w = ticket.stringWidth(data['company_name'], "DejaVu-Bold", 11)
        ticket.drawString((main_section_width - company_w) / 2, PAGE_HEIGHT - 22, data['company_name'])

        ticket.setFont("DejaVu-Bold", 8)
        unit_w = ticket.stringWidth(data['unit_name'], "DejaVu-Bold", 8)
        ticket.setFillColor(Color(0.3, 0.3, 0.3))
        ticket.drawString((main_section_width - unit_w) / 2, PAGE_HEIGHT - 34, data['unit_name'])

        # Title Badge Banner
        ticket.setFillColor(Color(0.15, 0.3, 0.18))
        ticket.rect(15, PAGE_HEIGHT - 100, main_section_width - 30, 22, fill=1, stroke=0)
        
        ticket.setFillColor(Color(1, 1, 1))
        ticket.setFont("DejaVu-Bold", 14)
        title_w = ticket.stringWidth(data['title'], "DejaVu-Bold", 14)
        ticket.drawString((main_section_width - title_w) / 2, PAGE_HEIGHT - 95, data['title'])

        # 5. Visitor Rules Card (Restored with proper Romanian diacritics)
        box_x = 15
        box_y = 15
        box_w = main_section_width - 30
        box_h = PAGE_HEIGHT - 130

        ticket.setFillColor(Color(0.96, 0.98, 0.96))
        ticket.setStrokeColor(Color(0.8, 0.85, 0.8))
        ticket.setLineWidth(0.5)
        ticket.roundRect(box_x, box_y, box_w, box_h, 4, fill=1, stroke=1)

        ticket.setFillColor(Color(0.15, 0.3, 0.18))
        ticket.setFont("DejaVu-Bold", 9)
        ticket.drawString(box_x + 10, box_y + box_h - 13, "Bucurați-vă de natură și relaxare!")

        ticket.setFillColor(Color(0.3, 0.3, 0.3))
        ticket.setFont("DejaVu", 6.5)
        ticket.drawString(box_x + 10, box_y + box_h - 22, "Vă dorim o drumeție minunată, aer curat și o experiență de neuitat pe trasee!")

        # Subtle separator line
        ticket.setStrokeColor(Color(0.85, 0.9, 0.85))
        ticket.setLineWidth(0.4)
        ticket.line(box_x + 10, box_y + box_h - 26, box_x + box_w - 10, box_y + box_h - 26)

        ticket.setFillColor(Color(0.2, 0.2, 0.2))
        ticket.setFont("DejaVu-Bold", 7.5)
        ticket.drawString(box_x + 10, box_y + box_h - 42, "Reguli esențiale de vizitare:")

        rules = [
            "• Păstrați curățenia și nu abandonați deșeuri pe trasee.",
            "• Respectați liniștea și protejați flora, fauna și formațiunile geologice.",
            "• Hrănirea urșilor și a altor animale sălbatice este strict interzisă.",
            "• Camparea este permisă exclusiv în locurile special amenajate.",
            "⚠️ Nerespectarea acestor reguli atrage sancțiuni conform legislației în vigoare.",
        ]
        
        rule_y = box_y + box_h - 54
        ticket.setFont("DejaVu", 7)
        for rule in rules:
            ticket.drawString(box_x + 10, rule_y, rule)
            rule_y -= 11

        # Website Footer
        ticket.setFillColor(Color(0.4, 0.4, 0.4))
        ticket.setFont("DejaVu-Bold", 8.5)
        web_w = ticket.stringWidth("www.bucegipark.ro", "DejaVu-Bold", 8.5)
        ticket.drawString((main_section_width - web_w) / 2, box_y + 6, "www.bucegipark.ro")

        # 6. Right-Hand Stub / Info Panel
        stub_x = PAGE_WIDTH - STUB_WIDTH
        
        ticket.setFillColor(Color(0.12, 0.18, 0.14))
        ticket.setStrokeColor(Color(0.15, 0.3, 0.18))
        ticket.rect(stub_x, 0, STUB_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        # 7. QR Code Frame
        qr_size = 48 * mm
        qr_x = stub_x + (STUB_WIDTH - qr_size) / 2
        qr_y = PAGE_HEIGHT - qr_size - 12
        
        ticket.setFillColor(Color(1, 1, 1))
        ticket.roundRect(qr_x - 4, qr_y - 4, qr_size + 8, qr_size + 8, 3, fill=1, stroke=0)

        qr = qrcode.QRCode(version=2, error_correction=ERROR_CORRECT_L, box_size=5, border=1)
        qr.add_data(data['qr'])
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_byte_io = BytesIO()
        qr_img.save(qr_byte_io, format='PNG')
        qr_byte_io.seek(0)

        ticket.drawImage(utils.ImageReader(qr_byte_io), qr_x, qr_y, width=qr_size, height=qr_size)

        # 8. Buyer Info & Expiry Meta Container
        meta_y = 12
        ticket.setFillColor(Color(0.2, 0.3, 0.22))
        ticket.roundRect(stub_x + 8, meta_y, STUB_WIDTH - 16, 38, 3, fill=1, stroke=0)

        ticket.setFillColor(Color(0.8, 0.9, 0.8))
        ticket.setFont("DejaVu-Bold", 7)
        ticket.drawString(stub_x + 14, meta_y + 26, "CUMPĂRĂTOR")
        
        ticket.setFillColor(Color(1, 1, 1))
        ticket.setFont("DejaVu-Bold", 8.5)
        buyer_name = f"{data['first_name']} {data['last_name']}".title()
        if len(buyer_name) > 28:
            buyer_name = buyer_name[:28] + "..."
        ticket.drawString(stub_x + 14, meta_y + 15, buyer_name)

        ticket.setFillColor(Color(0.8, 0.9, 0.8))
        ticket.setFont("DejaVu-Bold", 6.5)
        ticket.drawString(stub_x + 14, meta_y + 5, f"VALABIL PÂNĂ LA: {data['validity']}")

        # Finish page and save
        ticket.showPage()
        ticket.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    except Exception as e:
        print(f"Error generating PDF ticket: {e}")
        buffer.close()
        return None

if __name__ == "__main__":
    # for manual generation of a specific ticket for a buyer.
    
    series = "DBPNO2cb5cc"
    ticket_num = "039115" 
    
    data = {
        "qr": f"{series}{ticket_num}",
        "first_name": "Ian",    # Buyer's first name
        "last_name": "Huysman",  # Buyer's last name
        "file": f'ticket-{series}{ticket_num}.pdf',
        "series": series,
        "amount": 1,
        "validity": datetime.today().date() + timedelta(days=90),
        'title': "TICHET DE VIZITATOR",
        'background_image_path': str(SCRIPT_DIR / 'ticket_logos' / 'ticket_bg.png'),
        "bucegi_logo": str(SCRIPT_DIR / 'ticket_logos' / 'bucegi2.png'),
        "rnp_logo": str(SCRIPT_DIR / 'ticket_logos' / 'rnp-romsilva3.png'),
        "company_name": 'RNP ROMSILVA',
        "unit_name": 'ADMINISTRAȚIA PARCULUI NATURAL BUCEGI R.A.',
    }
    
    # Generate the polished PDF ticket bytes
    pdf = generate_pdf_ticket(data)
    
    if pdf:
        # Ensure the 'tickets' directory exists
        (SCRIPT_DIR / 'tickets').mkdir(parents=True, exist_ok=True)
        file_dest = SCRIPT_DIR / 'tickets' / f'ticket-{series}{ticket_num}.pdf'
        
        # Save to disk
        if save_pdf_to_location(pdf, file_dest):
            print(f"Successfully generated and saved manual ticket: {file_dest}")
        else:
            print("Failed to save PDF to disk.")
    else:
        print("PDF generation failed.")
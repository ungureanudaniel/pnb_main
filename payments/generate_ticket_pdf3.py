import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.core.files.base import ContentFile
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from .models import Ticket

## Create PDF with reportlab ##
def generate_pdf_ticket(data):
    
    # General Setup
    pdf_buffer = io.BytesIO()
    pagesize = (200*mm, 80*mm)
    c = canvas.Canvas(pdf_buffer, pagesize=pagesize)
    ticket=c.beginText()
    ticket.setTextOrigin(cm,cm)
    ticket.setFont('Helvetica', 14)

    ticket.drawImage(r"ticket_logos/ticket_bg.png", x=0, y=0,width=200, preserveAspectRatio=True, mask='auto')
    #add park logo
    ticket.drawImage(r'ticket_logos/bucegi2.png', x=175, y=4,width=22)
    #add company title
    ticket.drawString(145,10, r"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.")
    #add romsilva logo
    ticket.drawImage(r'ticket_logos/rnp-romsilva3.png', x=5, y=5,width=22)
    # add buyer
    ticket.drawString(10,30, f"Cumparator: {data['first_name'].title()} {data['last_name'].title()}")
    # add expiry date
    ticket.drawString(10,40,"Data expirarii: {}".format(data['date']))

    # Instantiate flowables
    
    # Append flowables and build doc
    
    # create and save pdf
    pdf_buffer.seek(0)    
    pdf = pdf_buffer.getvalue()
    file_data = ContentFile(ticket)
    pdf = Ticket(payment_id=data['payment_id'],buyer_fname=data['buyer_fname'],buyer_lname=data['buyer_lname'],ticket_series=data['ticket_series'],ticket_nr=data['ticket_nr'],ticket_pdf=file_data,ticket_type=data['ticket_nr'])
    pdf.save()
    response = FileResponse(pdf_buffer, as_attachment=True, filename=f"{data['ticket_id']}")
    
    return response
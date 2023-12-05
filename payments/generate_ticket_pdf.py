import os
from django.conf import settings
import random, string
from fpdf import FPDF
from django.http import FileResponse
import io
from django.utils.translation import gettext_lazy as _
#==========qr code module=========================
import qrcode
#============generate pdf ticket====================
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

#----------generate unique code for email subscription conf--------------------
def ticket_series(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
#----------generate unique code for email subscription conf--------------------
def ticket_nr(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

#=======================overrun FPDF class=====================
# class NEWPDF(FPDF):
#     def header(self):
#             self.image('bucegi2.png')
#             self.set_font('helvetica', 'BIU', 14)
#             self.cell(100,5,f"Header", align = "C", border=1)
#             self.cell(10,10,f"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.", ln=True, border=True)

#             self.ln(20)
#     def footer(self):
#             self.set_font('helvetica', 'BIU', 14)
#             self.cell(0,5,f"Footer", ln=True, border=1)
#             self.cell(10,10,f"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.", ln=True, border=True)

#             self.ln(20)
def generate_pdf_ticket(data:dict):
        
    ticket = FPDF('P','mm', format=(200,80))
    ticket.set_auto_page_break(auto=True, margin = 15)
    
    for i in range(1,int(data['amount'])): 
                ticket.add_page()
                #font
                #background watermark image
                ticket.image("ticket_logos/ticket_bg.png", x=0, y=0, w=200, h=80)                
                #add park logo
                ticket.set_xy(5,5)
                ticket.image('ticket_logos/bucegi2.png', w=22, h=19)
                
                #add header text
                ticket.set_font('Helvetica', 'BIU', 12)
                ticket.set_xy(29,10)
                ticket.cell(145,10, r"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.", align='C', ln=1, border=1)
                
                #add romsilva logo
                ticket.set_xy(175,4)
                ticket.image('ticket_logos/rnp-romsilva3.png', w=22, h=21)
                
                #
                ticket.set_xy(15,30)
                ticket.set_font('Helvetica', 'BIU', 12)
                ticket.cell(40,10, "{}: {} {}".format(data['buyer'],data['first_name'].title(), data['last_name'].title()))
                ticket.set_xy(175,4)
                #add QR code example
                # qr_code = qrcode.make(data['qr'])
                # qr_code = qrcode.QRCode(version = 1,
                #    box_size = 10,
                #    border = 5)
                # qr_code.add_data(data['qr'])
                # qr_code.make(fit = True)
                # img = qr_code.make_image(fill_color = 'black',
                #     back_color = '#2eb872')
                
                #add text
                
                ticket.set_xy(20,40)
                ticket.set_font('Helvetica', 'BIU', 12)
                ticket.cell(50,10,"{}: {}".format(data['ticketseries'],data['series']), ln=True, border=True)
                ticket.set_xy(70,30)
                ticket.cell(70,10,"{}: {} RON".format('Cost',data['amount']), ln=True, border=True)

            #export
    ticket.output(f"tickets/{data['file']}")
    return f"tickets/{data['file']}"
if __name__ == "__main__":
    y = 3
    x = 6
    file_nr = f"{ticket_nr(y)}" + f"{ticket_series(x)}"
    data = {
                        "qr": "u2y2hiuhf8o3q5u#fajl^akljas&8",
                        "first_name":'daniel',
                        "last_name":'ungureanu',
                        "file":f'ticket-{file_nr}.pdf',
                        "series":'DBPN0000001',
                        "amount": 3,
                        "buyer": "Cumpărător",
                        "ticketseries": "Serie tichet",
                    }
    generate_pdf_ticket(data)
# def generate_pdf_ticket(data:dict):
   
#     ticket = []
    
#     # Initialise the simple document template
#     doc = SimpleDocTemplate(f"{data['file']}",
#                             page_size=letter,
#                             bottomMargin=.4 * cm,
#                             topMargin=.4 * cm,
#                             rightMargin=.8 * cm,
#                             leftMargin=.8 * cm)
    
#     # set the font style
#     styles = getSampleStyleSheet()
#     styleN = styles['Normal']

#     p_count = Paragraph(f" Buyer Name: {data['first_name']} {data['last_name']} ")
#     ticket.append(Spacer(5, 20))
#     ticket.append(p_count)
#     # extract and add key value pairs to PDF
#     p = Paragraph("Numar si serie" + " : " + str(data['series']), styleN)
#     ticket.append(p)
#     ticket.append(Spacer(1, 2))
#     # build PDF using the data
#     doc.build(ticket)
#     doc.save()

#============generate the pdf file==================
# def create_ticket_pdf(file_name:str, series:str, extension:str):
#     c = canvas.Canvas(f"tickets/{file_name}{extension}", pagesize=letter)
#     c.setFillColor(colors.grey)
#     c.setFont("Helvetica-Bold", 24)
#     c.drawString(50, 700, "Visitor Ticket for Bucegi Natural Park")

#     c.setFillColor(colors.black)
#     c.setFont("Helvetica", 14)
#     c.drawString(50, 660, "REGIA NAȚIONALĂ A PĂDURILOR ROMSILVA R.A.")
#     c.drawString(50, 660, "ADMINISTRAȚIA PARCULUI NATURAL BUCEGI R.A.")

#     c.drawString(50, 640, series)
#     c.drawString(50, 620, "watermark")
#     c.drawString(50, 620, "contact info")


#     park_logo_path = os.path.join(os.getcwd(), r"C:\Users\ungur\Documents\code\pnb_main\static\img\logo\bucegi_logo.png")
#     rosilva_logo_path = os.path.join(os.getcwd(), r"C:\Users\ungur\Documents\code\pnb_main\static\img\logo\rnp-romsilva3.png")
    
#     c.drawImage(park_logo_path, 50, 400, width=150, height=150)
#     c.drawImage(rosilva_logo_path, 50, 400, width=150, height=150)
#     c.save()
# def generate_pdf_file(buyer_fname, buyer_lname,file_name:str, series:str, extension:str, adult_tickets:int):
#     from io import BytesIO
 
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
 
#     # Create a PDF document
#     p.drawString(100, 750, "Book Catalog")
 
#     y = 700
#     for i in range(0,adult_tickets):
#         p.drawString(100, y, f"Type: {series}")
#         p.drawString(100, y - 20, f"Author: {buyer_fname} {buyer_lname}")
#         p.drawString(100, y - 40, f"Year: {'sgfgfhgj'}")
#         y -= 60
 
#     p.showPage()
#     p.save()
 
#     buffer.seek(0)
#     return buffer

# def generate_pdf_ticket(buyer_fname, buyer_lname,file_name:str, series:str, adult_tickets:int):
#     #create bitestream buffer
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
#     textobj = c.beginText()
#     textobj.setTextOrigin(cm,cm)
#     textobj.setFont("Helvetica", 16)
#     #lines of text
#     lines = [
#         buyer_fname,
#         buyer_lname,
#         series,
#         "RNP ROMSILVA",

#     ]
#     #loop through each line
#     for line in lines:
#         textobj.textLine(line)
    
#     #finish generating 
#     c.drawText(textobj)
#     c.showPage()
#     c.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=file_name)


    
    
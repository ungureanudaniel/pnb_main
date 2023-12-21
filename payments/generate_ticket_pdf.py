from django.conf import settings
import random, string
from fpdf import FPDF, HTMLMixin
import qrcode
from django.http import FileResponse
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _
#==========qr code module=========================

#============generate pdf ticket====================

#----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)
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
class PDF(FPDF, HTMLMixin):
    pass
#loop through the number of tickets to be generated
# for i in range(1,int(data['amount'])):
def generate_pdf_ticket(data:dict):
        
    ticket = FPDF('P','mm', format=(200,80))
    ticket.set_auto_page_break(auto=True, margin = 2)
    ticket.add_page()
    #font
    #background watermark image
    ticket.image("ticket_logos/ticket_bg.png", x=0, y=0, w=200, h=80)                
    #add park logo
    ticket.set_xy(5,5)
    ticket.image('ticket_logos/bucegi2.png', w=22, h=19)
                
    #add header text
    ticket.set_font('helvetica', size =12)
    ticket.set_xy(29,10)
    ticket.cell(145,10, r"RNP ROMSILVA - ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.", align='C', border=1)
                
    #add romsilva logo
    ticket.set_xy(175,4)
    ticket.image('ticket_logos/rnp-romsilva3.png', w=22, h=21)
                
    # add buyer name
    ticket.set_xy(10,30)
    ticket.set_font('helvetica', size =12)
    ticket.cell(90,10, f"Cumparator: {data['first_name'].title()} {data['last_name'].title()}")
    # add expiry date
    ticket.set_xy(10,40)
    ticket.cell(70,10,"Data expirarii: {}".format(data['date']), border=True)
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
    # add ticket series
    # ticket.set_xy(10,40)
    # ticket.set_font('helvetica', size = 12)
    # ticket.cell(90,10,"{}: {}".format(data['ticketseries'],data['series']), border=True)
    # add bar code created using ticket series
    # ticket.code39(f"*{data['series']}*", x=120, y=30, w=1, h=10)
    img = qrcode.make(f"{data['series']}")
    ticket.image(img.get_image(), x=145, y=25, w=50, h=50)
    ticket.set_xy(155,70)
    ticket.set_font('helvetica', size = 8)
    ticket.write(5,"{}".format(data['series']))
    # add Cost to ticket
    ticket.set_xy(10,50)
    ticket.set_font('helvetica', size = 12)
    ticket.cell(70,10,"{}: {} RON".format('Cost',data['amount']), border=False)
    #add Cost to ticket
    ticket.set_xy(10,58)
    ticket.set_font('Helvetica', size=6)
    ticket.multi_cell(130,3,"*Acest tarif de vizitare este instituit conform O.U.G. 57 / 2007, cu modificarile si completarile ulterioare, art. 30, alin. (3) si ordinul Nr. 3836 / 2012 privind aprobarea Metodologiei de avizare a tarifelor instituite de catre administratorii ariilor naturale protejate pentru vizitarea acestora.")
    #add website
    ticket.set_xy(70,66)
    ticket.cell(70,10,"Web: www.bucegipark.ro",link="https://www.bucegipark.ro")
    ticket.set_xy(110,66)
    ticket.cell(70,10,"Email: contact@bucegipark.ro",link="mailto:contact@bucegipark.ro")            
    #export
    ticket.output("tickets/{}".format(data['file']))
    return "tickets/{}".format(data['file'])
if __name__ == "__main__":
    y = 3
    x = 6
    series='DBPNO000001'
    file_nr = f"{series}{ticket_series()}"
    data = {
                        "first_name":'daniel',
                        "last_name":'ungureanu',
                        "file":'ticket-{}.pdf'.format(file_nr),
                        "series":'https://bucegipark.ro',
                        "amount": 10,
                        "date": datetime.today().date() + timedelta(days=90),
                        "ticketseries": "Serie tichet",
                    }
    generate_pdf_ticket(data)


    
    
from django.http import FileResponse
from reportlab.pdfgen import canvas
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _
# def generate_pdf(request):
#     response = FileResponse(generate_pdf_file(), 
#                             as_attachment=True, 
#                             filename='book_catalog.pdf')
#     return response
 #----------generate unique code for email subscription conf--------------------
def ticket_series():
    return ''.join(datetime.now().strftime('%Y%m%d%H%M%S')
)
#----------generate unique code for email subscription conf--------------------
def ticket_nr(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
 
def generate_pdf_ticket(data):
    from io import BytesIO
 
    buffer = BytesIO()
    ticket = canvas.Canvas(buffer)
     # Create a PDF document
    #add background image
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
    # for i in books:
    #     p.drawString(100, y, f"Title: {book.title}")
    #     p.drawString(100, y - 20, f"Author: {book.author}")
    #     p.drawString(100, y - 40, f"Year: {book.publication_year}")
    #     y -= 60
 
    ticket.showPage()
    ticket.save()
 
    buffer.seek(0)
    return buffer

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
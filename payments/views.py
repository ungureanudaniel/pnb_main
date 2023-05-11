from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
import random, string
import datetime
from django.utils.text import slugify
#----------generate unique code for email subscription conf--------------------
def random_ticket_nr():
    return "%0.12d" % random.randint(0, 99999999)
#----------generate unique code for email subscription conf--------------------
def random_series(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
#===============the ticket description view======================
def ticketpay_view(request):
    template = "payments/ticket-online.html"
    context = {}
    # if request.method=='POST':
    #     try:
    #         tickets = request.POST['tickets_nr']
    #         print("tickets:",tickets)
    #         context = {
    #             "tickets": tickets,
    #         }
    #     except Exception as e:
    #         messages.warning(request, _(f"Failed! {e}"))

    return render(request, template, context)
#===============the ticket checkout view======================
def checkout_view(request):
    template = "payments/ticket-checkout.html"
    context = {

    }
    if request.method=='POST':
        tickets = int(request.POST.get('tickets_nr'))
        price = float(request.POST.get('total_price'))
        print("tickets:",tickets)
        fname = request.POST.get('first-name')
        lname = request.POST.get('last-name')
        phone = request.POST.get('phone-number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        county = request.POST.get('county')
        country = request.POST.get('country-select')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        note = request.POST.get('notes')
        code = f"{random_series(3).upper()}"+ " " + f"{random_ticket_nr()}"
        print(code)
        #=============save new payment in database ============
        try:
            new_pay = Payment(payment_code=code, sum=price, buyer_fname=fname, buyer_lname=lname, phone=phone, email=email, address=address, county=county, country=country, city=city,zip=zip, notes=note, timestamp=datetime.datetime.now())
            new_pay.slug = slugify(code)
            new_pay.save()
        except Exception as e:
            messages.warning(request, _(f"Warning! Payment functionalities disabled and under maintenance."))
        #=============loop through the number of tickets and generate tickets pdf========
        for ticket in range(1, tickets+1):
            new_ticket = Ticket()
        context.update({
            "tickets": tickets,
            "price": price,
        })


    return render(request, template, context)

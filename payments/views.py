from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
import random, string
import datetime
from django.utils.text import slugify
import warnings 
warnings.filterwarnings('ignore', message='.*cryptography', )
#--------------netopia payment imports-----------------
from urllib.parse import unquote, quote
import requests
import hashlib
import random
import time
from payments.address import Address
from payments.invoice import Invoice
from payments.request import Request
from payments.payment.request.crc import Crc
from payments.payment.request.card import Card
from payments.payment.request.base_request import BaseRequest
from payments.client import get_and_send_request
#------------netopia payments imports end-------------

#----------generate unique code for email subscription conf--------------------
def random_ticket_nr():
    return "%0.12d" % random.randint(0, 99999999)
#----------generate unique code for email subscription conf--------------------
def random_series(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
#===============the ticket description view======================
def choosetickets_view(request):
    template = "payments/choose-tickets.html"
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
# def checkout_view(request):
#     payment_url = 'https://sandboxsecure.mobilpay.ro'
#     template = "payments/ticket-checkout.html"
#     context = {

#     }
#     if request.method=='POST':
#         tickets = int(request.POST.get('tickets_nr'))
#         price = float(request.POST.get('total_price'))
#         print("tickets:",tickets)
#         fname = request.POST.get('first-name')
#         lname = request.POST.get('last-name')
#         phone = request.POST.get('phone-number')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         county = request.POST.get('county')
#         country = request.POST.get('country-select')
#         city = request.POST.get('city')
#         zip = request.POST.get('zip')
#         note = request.POST.get('notes')
#         # code = f"{random_series(3).upper()}"+ " " + f"{random_ticket_nr()}"
#         # print(code)

#         # data according to implementation suggestion by netopia

#         # =============save new payment in database ============
#         try:
#             new_pay = Payment(payment_code=code, sum=price, buyer_fname=fname, buyer_lname=lname, phone=phone, email=email, address=address, county=county, country=country, city=city,zip=zip, notes=note, timestamp=datetime.datetime.now())
#             new_pay.slug = slugify(code)
#             new_pay.save()
#         except Exception as e:
#             messages.warning(request, _(f"Warning! Payment functionalities disabled and under maintenance."))
#         #=============loop through the number of tickets and generate tickets pdf========
#         for ticket in range(1, tickets+1):
#             new_ticket = Ticket()
#         context.update({
#             "tickets": tickets,
#             "price": price,
#         })

#         try:
#             data, key = get_and_send_request()

#             r = requests.post(payment_url,
#                             data={'env_key': key, 'data': data})
#             # get status code
#             print(f"mobilpay status code is:{r.status_code}, {r.reason}")
#             # print response
#             print(f"response from mobilpay is:{r.text}")

#         except Exception as e:
#             # catch any error that occured
#             print(e.args)
#     return render(request, template, context)

#==============ticket checkout and post request to Payment processor========================================
def checkout_view(request):
    template = "payments/ticket-checkout.html"
    #------netopia payments specific test url------------------
    payment_url = 'https://sandboxsecure.mobilpay.ro'
    #------path to public certificate that contains the public key
    x509_filePath = r"payments\util\mobilpay_pubkey.cer"
    #---------create Card instance from the class designed in mobilpay folder-------
    obj_pm_req_card = Card()

    context = {}
    if request.method=='POST':
        try:
            obj_pm_req_card.set_signature("<signature>")

            # order id
            obj_pm_req_card.set_order_id(
                hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())
            obj_pm_req_card.set_confirm_url("NULL")
            obj_pm_req_card.set_return_url("pay-return")
            obj_pm_req_card.set_invoice(Invoice())
            obj_pm_req_card.get_invoice().set_currency("RON")
            obj_pm_req_card.get_invoice().set_amount(float(request.POST.get('total_price')))
            obj_pm_req_card.get_invoice().set_token_id("<TokenId>")
            obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")
            billing_address = Address("billing")
            print(f"The payer data is here: {obj_pm_req_card.get_invoice()}")
            # get_from_website
            billing_address.set_type("person")
            billing_address.set_first_name(request.POST.get('first-name'))
            billing_address.set_last_name(request.POST.get('last-name'))
            billing_address.set_address(request.POST.get('address'))
            billing_address.set_email(request.POST.get('email'))
            billing_address.set_mobile_phone(request.POST.get('phone-number'))

            obj_pm_req_card.get_invoice().set_billing_address(billing_address)
            print(f"The billing address: {billing_address}")
            # shipping_address = Address("shipping")
            # get_from_website
            # shipping_address.set_type("person")
            # shipping_address.set_first_name("Netopia")
            # shipping_address.set_last_name("Payments")
            # shipping_address.set_address("Pipera")
            # shipping_address.set_email(request.POST.get('email'))
            # shipping_address.set_mobile_phone(request.POST.get('phone-number'))


            # obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

            """encoded data and env_key"""
            obj_pm_req_card.encrypt(x509_filePath)
            data = obj_pm_req_card.get_enc_data()
            env_key = obj_pm_req_card.get_env_key()

            try:
                # data, key = get_and_send_request()
                r = requests.post(payment_url,
                                data={'env_key': env_key, 'data': data})
                # get status code
                print(r.status_code, r.reason)
                # print response
                print(r.text)

            except Exception as e:
                # catch any error that occured
                print(e.args)

            return data, env_key

        except Exception as e:
            raise Exception(e)
        
def pay_confirm_view(request):
    template = "payments\payment-confirmation.html"
    context = {}
    return render(request, template, context)
def pay_return_view(request):
    template = "payments\payment-return.html"
    context = {}
    return render(request, template, context)


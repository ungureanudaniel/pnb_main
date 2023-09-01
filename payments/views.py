from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PaymentForm
import random, string
from django.urls import reverse
import datetime
from django.conf import settings
from django.utils.text import slugify
import warnings 
warnings.filterwarnings('ignore', message='.*cryptography', )
#--------------netopia payment imports-----------------
from urllib.parse import unquote, quote
import requests
import hashlib
import random
import time
from payments.netopia.address import Address
from payments.netopia.invoice import Invoice
from payments.netopia.request import Request
from payments.netopia.payment.request.crc import Crc
from payments.netopia.payment.request.card import Card
from payments.netopia.payment.request.base_request import BaseRequest
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
    if request.method=='POST':
        try:
            request.session['price'] = request.POST.get('total_price') # set 'total_price' in the session
            request.session['tickets'] = request.POST.get('tickets_nr') # set 'tickets_nr' in the session

            context = {
                "tickets":request.POST.get('tickets_nr'),
                "price":request.POST.get('total_price'),
            }
            return redirect("checkout")
        except Exception as e:
            messages.warning(request, _(f"Failed! {e}"))
            return render(request,template,context)

       
    return render(request,template,context)
#=================payments-view=================================
def payment_processing(request):
    return render(action, template, context)


# ==============ticket checkout and post request to Payment processor========================================
def checkout_view(request):
    template = "payments/ticket-checkout.html"
#     payment_url = settings.PAYMENT_SANDBOX_URL
#     #assign form instance to variable
#     form = PaymentForm(request.POST or None)
#     price = request.session['price']
#     tickets = request.session['tickets']

#     print(price)
#     context = {
#         "form":form,
#         "price":price,
#         "tickets":tickets,
#     }
#     #all good up to here
#     if request.method=='POST':
#         try:
#             if form.is_valid():
#                 form.save()
#                 #request to payment provider
#                 try:
#                     data, key = get_and_send_request()
#                     print(data,key)
#                     r = requests.post(payment_url,
#                                     data={'env_key': key, 'data': data})
#                     # get status code
#                     print(r.status_code, r.reason)
#                     # print response
#                     print(r.text)

#                 except Exception as e:
#                     # catch any error that occured
#                     print(e.args)
#         except Exception as e:
#                 # catch any error that occured
#                 print(e.args)

          
#     return render(request,template,context)
    # ------netopia payments specific test url------------------
    payment_url = 'https://sandboxsecure.mobilpay.ro'
    #------path to public certificate that contains the public key
    x509_filePath = r"payments\netopia_certif\sandbox.2RB1-THZT-LU8F-R4R3-O4RH.public.cer"
    #---------create Card instance from the class designed in mobilpay folder-------
    obj_pm_req_card = Card()
    #assign form instance to variable
    form = PaymentForm(request.POST or None)
    #fetch ticket nr and price from session
    price = request.session['price']
    tickets = request.session['tickets']
    
    #all good up to here
    if request.method=='POST':
        if form.is_valid():
            print(f"Form is valid!Nr of ticket {tickets}, price {price}")
            try:
                # fetch signature code 
                obj_pm_req_card.set_signature("payments\netopia_certif\signature.cer")
            except Exception as e:
                raise Exception(e)
            try:
                # generate order id
                obj_pm_req_card.set_order_id(
                        hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())
            except Exception as e:
                raise Exception(e)
            new_payment=form.save(commit=False)
            new_payment.payment_id = obj_pm_req_card.get_order_id()
            new_payment.save()
            
            try:
                
                
                obj_pm_req_card.set_confirm_url("pay-confirm")
                obj_pm_req_card.set_return_url("pay-return")
                obj_pm_req_card.set_invoice(Invoice())
                obj_pm_req_card.get_invoice().set_currency("RON")
                obj_pm_req_card.get_invoice().set_amount(price)
                obj_pm_req_card.get_invoice().set_token_id("<TokenId>")
                obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")
                billing_address = Address("billing")
                print(f"The payer data is here: {obj_pm_req_card.get_invoice()}")
                # get_from_website
                billing_address.set_type("person")
                billing_address.set_first_name(form.cleaned_data['buyer_fname'])
                billing_address.set_last_name(form.cleaned_data['buyer_lname'])
                billing_address.set_address(form.cleaned_data['address'])
                billing_address.set_email(form.cleaned_data['email'])
                billing_address.set_mobile_phone(form.cleaned_data['phone'])

                obj_pm_req_card.get_invoice().set_billing_address(billing_address)
                print(f"The billing address: {billing_address}")
                shipping_address = Address("shipping")
                # get_from_website
                shipping_address.set_type("person")
                shipping_address.set_first_name(form.cleaned_data['buyer_fname'])
                shipping_address.set_last_name(form.cleaned_data['buyer_lname'])
                shipping_address.set_address("None")
                shipping_address.set_email(form.cleaned_data['email'])
                shipping_address.set_mobile_phone(form.cleaned_data['phone'])


                obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

                """encoded data and env_key"""
                obj_pm_req_card.encrypt(x509_filePath)
                data = obj_pm_req_card.get_enc_data()
                env_key = obj_pm_req_card.get_env_key()
                print("The env_key is:{}".format(env_key))
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
                print(obj_pm_req_card.get_invoice())
                return redirect("https://sandboxsecure.mobilpay.ro/", data)

            except Exception as e:
                raise Exception(e)
        else:
            return redirect("pay-failure")
    #add form and ticket +price to context var
    context = {
        "form":form,
        "price":price,
        "tickets":tickets,
    }
    return render(request, template, context)
        
def pay_success_view(request):
    template = "payments\payment-success.html"
    context = {}
    return render(request, template, context)
def pay_failure_view(request):
    template = "payments\payment-failure.html"
    context = {}
    return render(request, template, context)


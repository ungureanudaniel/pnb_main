from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt
import random, string
from django.urls import reverse
import datetime
from django.conf import settings
from django.utils.text import slugify
import warnings
from django.http import JsonResponse

warnings.filterwarnings('ignore', message='.*cryptography', )
#--------------netopia payment imports-----------------
# from urllib.parse import unquote, quote
# import requests
# import hashlib
# import random
# import time
# from payments.netopia.address import Address
# from payments.netopia.invoice import Invoice
# from payments.netopia.request import Request
# from payments.netopia.payment.request.crc import Crc
# from payments.netopia.payment.request.card import Card
# from payments.netopia.payment.request.base_request import BaseRequest
# from payments.client import get_and_send_request
#------------euplatesc imports--------------------------------
import hashlib 
import hmac
import uuid
from time import strftime

#----------generate unique code for email subscription conf--------------------
def random_ticket_nr():
    return "%0.12d" % random.randint(0, 99999999)
#-----------------generate euplatesc hash -------------------
def euplatesc_mac(key,params):
    data=""
    for p in params:
        if len(p)==0:
            data+="-"
        else:
            data+=str(len(p))+p
   
    print(data)
    print("\n")

    return hmac.new(bytes.fromhex(key),data.encode(),hashlib.md5).hexdigest().upper()
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

            return redirect("checkout")
        except Exception as e:
            messages.warning(request, _(f"Failed! {e}"))
            return render(request,template,context)
    return render(request,template,context)
#=================payments-view=================================
def payment_processing(request):
    return render(request, template, context)


# ==============ticket checkout and post request to Payment processor========================================

# def checkout_view(request):
#     template = "payments/ticket-checkout.html"
#     # ------netopia payments specific test url------------------
#     payment_url = 'https://sandboxsecure.mobilpay.ro'
#     #------path to public certificate that contains the public key
#     x509_filePath = r"payments\netopia_certif\sandbox.2RB1-THZT-LU8F-R4R3-O4RH.public.cer"
#     #---------create Card instance from the class designed in mobilpay folder-------
#     obj_pm_req_card = Card()
    
#     #fetch ticket nr and price from session
#     price = request.session['price']
#     tickets = request.session['tickets']
#     #assign form instance to variable
#     form = PaymentForm(request.POST or None)
#     #all good up to here
#     # logic for when users click pay button
#     if request.method=='POST':
#         if form.is_valid():
#             print(f"Form is valid!Nr of ticket {tickets}, price {price}")
#             try:
#                 # fetch signature  
#                 obj_pm_req_card.set_signature("payments\netopia_certif\signature.cer")
#             except Exception as e:
#                 raise Exception(e)
#             try:
#                 # generate order id
#                 obj_pm_req_card.set_order_id(
#                         hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())
#             except Exception as e:
#                 raise Exception(e)
#             new_payment=form.save(commit=False)
#             new_payment.payment_id = "1234test"
#             new_payment.save()
            
#             try:
                
                
#                 obj_pm_req_card.set_confirm_url("pay-confirm")
#                 obj_pm_req_card.set_return_url("pay-return")
#                 obj_pm_req_card.set_invoice(Invoice())
#                 obj_pm_req_card.get_invoice().set_currency("RON")
#                 obj_pm_req_card.get_invoice().set_amount(price)
#                 obj_pm_req_card.get_invoice().set_token_id("<TokenId>")
#                 obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")
#                 billing_address = Address("billing")
#                 print(f"The payer data is here: {obj_pm_req_card.get_invoice()}")
#                 # get_from_website
#                 billing_address.set_type("person")
#                 billing_address.set_first_name(form.cleaned_data['buyer_fname'])
#                 billing_address.set_last_name(form.cleaned_data['buyer_lname'])
#                 billing_address.set_address(form.cleaned_data['address'])
#                 billing_address.set_email(form.cleaned_data['email'])
#                 billing_address.set_mobile_phone(form.cleaned_data['phone'])

#                 obj_pm_req_card.get_invoice().set_billing_address(billing_address)
#                 print(f"The billing address: {billing_address}")
#                 shipping_address = Address("shipping")
#                 # get_from_website
#                 shipping_address.set_type("person")
#                 shipping_address.set_first_name(form.cleaned_data['buyer_fname'])
#                 shipping_address.set_last_name(form.cleaned_data['buyer_lname'])
#                 shipping_address.set_address("None")
#                 shipping_address.set_email(form.cleaned_data['email'])
#                 shipping_address.set_mobile_phone(form.cleaned_data['phone'])


#                 obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

#                 """encoded data and env_key"""
#                 obj_pm_req_card.encrypt(x509_filePath)
#                 data = obj_pm_req_card.get_enc_data()
#                 env_key = obj_pm_req_card.get_env_key()
#                 print("The env_key is:{}".format(env_key))
#                 try:
#                     # data, key = get_and_send_request()
#                     r = requests.post(payment_url,
#                                     data={'env_key': env_key, 'data': data})
#                     # get status code
#                     print(r.status_code, r.reason)
#                     # print response
#                     print(r.text)
                    
#                 except Exception as e:
#                     # catch any error that occured
#                     print(e.args)
#                 print(obj_pm_req_card.get_invoice())
#                 return redirect("https://sandboxsecure.mobilpay.ro/", data)

#             except Exception as e:
#                 print("e")
#                 raise Exception(e)
#         else:
#             print(form.errors.as_data())
#             return redirect("pay-failure")
#     #add form and ticket +price to context var
    # context = {
    #     "form":form,
    #     "price":price,
    #     "tickets":tickets,
    # }
    # return render(request, template, context)
@csrf_exempt
def checkout_view(request):
    template = "payments/ticket-checkout.html"
    #fetch ticket nr and price from session
    price = request.session['price']
    tickets = request.session['tickets']
    
    
    #euplatesc account credentials
    key="00112233445566778899AABBCCDDEEFF"
    mid="testaccount"
    params= {}
    if request.method=='POST':
        #assign form instance to variable
        form = PaymentForm(request.POST or None, initial={"price": price, "quantity": tickets})

        # form = PaymentForm(initial={'quantity': tickets,'price': price})
        if form.is_valid():
            try:
                new_payment=form.save(commit=False)
                new_payment.payment_id = "1234test"
                new_payment.save()
                #euplatesc parameters
                params={
                    'amount':price,
                    'curr':'RON',
                    'invoice_id':random_ticket_nr(),
                    'order_desc':'Test order Bucegi',
                    'merch_id':mid,
                    'timestamp':strftime("%Y%m%d%H%M%S"),
                    'nonce': uuid.uuid4().hex
                }
                oparam=[params['amount'],params['curr'],params['invoice_id'],params['order_desc'],params['merch_id'],params['timestamp'],params['nonce']]
                params['fp_hash']=euplatesc_mac(key,oparam)
                print(f"Form is valid!Nr of ticket {tickets}, price {price} and parameters are:{params['fp_hash']}")
                return JsonResponse("https://secure.euplatesc.ro/tdsprocess/tranzactd.php", data = oparam)
            except Exception as e:
                print("e")
                messages.warning(request, _(f"Failed! {e}"))
                raise Exception(e)    
        else:
            print(form.errors.as_data())
            messages.warning(request, f"Something went wrong. Please try again! ({form.errors.as_data()})")
            return redirect("checkout")
    else:
        form = PaymentForm()
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


    
	
    
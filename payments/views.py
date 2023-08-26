from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PaymentForm
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
#=================payments-view=================================
def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )

# ==============ticket checkout and post request to Payment processor========================================
def checkout_view(request):
    template = "payments/ticket-checkout.html"
    
    form = PaymentForm(request.POST or None)
    context = {
        "form":form,
    }
    if request.method=='POST':
        if form.is_valid():

            r = get_and_send_request()
            print(r)
            context.update(r)
    return render(request,template,context)
    #------netopia payments specific test url------------------
    # payment_url = 'https://sandboxsecure.mobilpay.ro'
    # #------path to public certificate that contains the public key
    # x509_filePath = r"payments\util\mobilpay_pubkey.cer"
    # print(x509_filePath)
    # #---------create Card instance from the class designed in mobilpay folder-------
    # obj_pm_req_card = Card()
    # form = Payment
    # context = {}
    # if request.method=='POST':
    #     try:
    #         obj_pm_req_card.set_signature("<signature>")

    #         # order id
    #         obj_pm_req_card.set_order_id(
    #             hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())
    #         obj_pm_req_card.set_confirm_url("pay-confirm")
    #         obj_pm_req_card.set_return_url("pay-return")
    #         obj_pm_req_card.set_invoice(Invoice())
    #         obj_pm_req_card.get_invoice().set_currency("RON")
    #         obj_pm_req_card.get_invoice().set_amount(float(request.POST.get('total_price')))
    #         obj_pm_req_card.get_invoice().set_token_id("<TokenId>")
    #         obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")
    #         billing_address = Address("billing")
    #         print(f"The payer data is here: {obj_pm_req_card.get_invoice()}")
    #         # get_from_website
    #         billing_address.set_type("person")
    #         billing_address.set_first_name(request.POST.get('first-name'))
    #         billing_address.set_last_name(request.POST.get('last-name'))
    #         billing_address.set_address(request.POST.get('address'))
    #         billing_address.set_email(request.POST.get('email'))
    #         billing_address.set_mobile_phone(request.POST.get('phone-number'))

    #         obj_pm_req_card.get_invoice().set_billing_address(billing_address)
    #         print(f"The billing address: {billing_address}")
    #         shipping_address = Address("shipping")
    #         # get_from_website
    #         shipping_address.set_type("person")
    #         shipping_address.set_first_name(request.POST.get('first-name'))
    #         shipping_address.set_last_name(request.POST.get('last-name'))
    #         shipping_address.set_address("None")
    #         shipping_address.set_email(request.POST.get('email'))
    #         shipping_address.set_mobile_phone(request.POST.get('phone-number'))


    #         obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

    #         """encoded data and env_key"""
    #         obj_pm_req_card.encrypt(x509_filePath)
    #         data = obj_pm_req_card.get_enc_data()
    #         env_key = obj_pm_req_card.get_env_key()
    #         print("The env_key is:{}".format(env_key))
    #         try:
    #             # data, key = get_and_send_request()
    #             r = requests.post(payment_url,
    #                             data={'env_key': env_key, 'data': data})
    #             # get status code
    #             print(r.status_code, r.reason)
    #             # print response
    #             print(r.text)
                
    #         except Exception as e:
    #             # catch any error that occured
    #             print(e.args)
    #         print(obj_pm_req_card.get_invoice())
    #         return render(request, template, {"env_key":env_key, "data":data, "price":"1010"})

    #     except Exception as e:
    #         raise Exception(e)
        
def pay_success_view(request):
    template = "payments\payment-success.html"
    context = {}
    return render(request, template, context)
def pay_failure_view(request):
    template = "payments\payment-failure.html"
    context = {}
    return render(request, template, context)


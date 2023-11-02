from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ticket, Payment
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt
import random, string
from django.urls import reverse
from django.utils import timezone
import datetime
from django.conf import settings
from django.utils.text import slugify
import warnings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode

warnings.filterwarnings('ignore', message='.*cryptography', )
#------------euplatesc imports--------------------------------
import hashlib 
import hmac
import uuid
from time import strftime

#----------generate unique code for email subscription conf--------------------
def ticket_nr():
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
# def choosetickets_view(request):
#     template = "payments/choose-tickets.html"
#     context = {}
#     if request.method=='POST':
#         try:
#             request.session['price'] = request.POST.get('total_price') # set 'total_price' in the session
#             request.session['tickets'] = request.POST.get('tickets_nr') # set 'tickets_nr' in the session

#             return redirect("checkout")
#         except Exception as e:
#             messages.warning(request, _(f"Failed! {e}"))
#             return render(request,template,context)
#     return render(request,template,context)
#================= checkout view =========================
@login_required
def checkout_view(request):
    template = "payments/ticket-checkout.html"
    #fetch ticket nr and price from session
    # price = request.session.get('price')
    # quantity = request.session.get('tickets')
    #euplatesc account credentials
    key="00112233445566778899AABBCCDDEEFF"
    mid="testaccount"
    params= {}
    #assign form instance to variable
    form = PaymentForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            try:
                #save payment to database
                new_payment=form.save(commit=False)
                new_payment.timestamp = timezone.now()
                new_payment.save()
                #euplatesc parameters
                params={
                    'amount':str(1),
                    'curr':'RON',
                    'invoice_id':str(new_payment.payment_id),
                    'order_desc':'Test order Bucegi',
                    'merch_id':mid,
                    'timestamp':strftime("%Y%m%d%H%M%S"),
                    'nonce': uuid.uuid4().hex
                }
                oparam=[params['amount'],params['curr'],params['invoice_id'],params['order_desc'],params['merch_id'],params['timestamp'],params['nonce']]
                params['fp_hash']=euplatesc_mac(key,oparam)
                # print(f"Form is valid!Nr of ticket {new_payment.quantity}, price {new_payment.price} and parameters are:{params['fp_hash']}")
                
                #----create a url with the parameters in it  and redirect to it
                params['ExtraData[silenturl]']='https://bucegipark.ro/en/tickets/status'
                query_string = urlencode(params)
                payment_url=f'https://secure.euplatesc.ro/tdsprocess/tranzactd.php?{query_string}'
                print(f"post data is: {request.POST}")
                print(f"post data is: {params}")

                return redirect(payment_url)
                
            except Exception as e:
                print(e)
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
            # "price":price,
            # "tickets":quantity,
            }
    return render(request, template, context)

#============call back url=====================	
def pay_callback(request):
	#aici se va actualiza statusul payment-ului
	#in POST se va primi parametrul invoice_id
	#iar daca parametrul action=0 atunci plata este cu success
	#...
    template_success= "payments\payment-success.html"
    template_failure="payments\payment-failure.html"
    try:
        invoice_id = request.GET['invoice_id']
        print(f"Invoice id is: {invoice_id}")
        payment_id = Payment.objects.get(payment_id=request.GET['invoice_id'])
        print(payment_id)
        if request.action == "0":
        
            return render(request, "https://bucegipark.ro/en/tickets/status/", {'status': 'successful'})
    except Exception as e:
        messages.warning(request, e)
        return render(request, template_failure, {'status': 'failed'})
    return render(request, "", {})
#=============payment callback data=========================
#crsf token exempted in urls.py
def check_status(request):
    if request.method == 'POST':
        messages.warning(request, request.POST)
        print(f"callback data is: {request.POST}")# examine the data returned from the API
#==============pay_success_view=================
def pay_success_view(request):
    template = "payments\payment-success.html"
    context = {}
    return render(request, template, context)
#==============pay_failure_view=================
def pay_failure_view(request):
    template = "payments\payment-failure.html"
    context = {}
    return render(request, template, context)


    
	
    
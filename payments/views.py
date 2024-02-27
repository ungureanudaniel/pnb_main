from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Payment, Ticket
from django.shortcuts import redirect, render
from .forms import PaymentForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from email.mime.base import MIMEBase
from email import encoders
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
import warnings
from .forms import CaptchaForm
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
#-----------invoice and ticket generation imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from .generate_ticket_pdf2 import generate_pdf_ticket, save_pdf_to_location

#--------------------------------------------------
warnings.filterwarnings('ignore', message='.*cryptography', )
#------------euplatesc imports--------------------------------
import hashlib 
import hmac
import uuid
from time import strftime

#----------generate unique code for invoice and ticket--------------------

#-----------------generate euplatesc hash -------------------
def euplatesc_mac(key,params):
    data=""
    for p in params:
        if len(p)==0:
            data+="-"
        else:
            data+=str(len(p))+p
   
    # print(data)
    # print("\n")

    return hmac.new(bytes.fromhex(key),data.encode(),hashlib.md5).hexdigest().upper()
#----------generate unique code for email subscription conf--------------------
# def ticket_series(y):
#     return ''.join(random.choice(string.ascii_letters) for x in range(y))
# #----------generate unique code for email subscription conf--------------------
# def ticket_nr(y):
#     return ''.join(random.choice(string.ascii_letters) for x in range(y))

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
    #-------->MUST EDIT THIS to fetch ticket nr and price from session and not hardcoded<------- !!!!!!
    # price = request.session.get('price')
    # quantity = request.session.get('tickets')
    #-------->MUST EDIT THIS to fetch ticket nr and price from session and not hardcoded<------- !!!!!!

    #euplatesc account credentials ==== must be imported for env variable in production !!!!!!!!!!!
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
                if new_payment.quantity > 0:

                    new_payment.timestamp = timezone.now()
                    new_payment.save()
                    #----euplatesc parameters
                    params={
                        # 'amount':str(new_payment.price),
                        #=============switch the amount param to take new_payment.price======================================!!!!!!!!!!!
                        'amount': '1',
                        'curr':'RON',
                        'invoice_id':str(new_payment.payment_id),
                        #==========need to change this in production=========================================================!!!!!!!!!!!
                        'order_desc':'Test order Bucegi',
                        'merch_id':mid,
                        'timestamp':strftime("%Y%m%d%H%M%S"),
                        'nonce': uuid.uuid4().hex
                    }
                    oparam=[params['amount'],params['curr'],params['invoice_id'],params['order_desc'],params['merch_id'],params['timestamp'],params['nonce']]
                    params['fp_hash']=euplatesc_mac(key,oparam)
                    # print(f"Form is valid!Nr of ticket {new_payment.quantity}, price {new_payment.price} and parameters are:{params['fp_hash']}")
                    
                    #----add parameters for post data server to server and for redirection to merchant site
                    params['ExtraData[silenturl]']=f'{settings.BASE_URL}/en/tickets/status/'
                    params['ExtraData[successurl]']=f'{settings.BASE_URL}/en/tickets/payment-success/'
                    params['ExtraData[failedurl]']=f'{settings.BASE_URL}/en/tickets/payment-failure/'
                    params['ExtraData[backtosite]']=f'{settings.BASE_URL}/tickets/payment-checkout/'
                    query_string = urlencode(params)
                    payment_url=f'https://secure.euplatesc.ro/tdsprocess/tranzactd.php?{query_string}'
                    return redirect(payment_url)
                #functionality for separate kids tickets
                # elif new_payment.quantity == 0 and new_payment.quantity_kids > 0:
                #     messages.success(request, _("Your children tickets have been sent to the email you provided. Your kids should always have the tickets with them when visiting Bucegi Natural Park. Thank you!"))
                #     return redirect("pay-success")
                else:
                    messages.warning(request, _("You must choose at least one ticket to finalize the purchase."))
                    return redirect("checkout")
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
#=============payment callback data=========================
def check_status(request):
    """
    This function, check_status, is responsible for handling payment status updates received from a payment provider server in a Django web application.

    Process Overview:
    1. Request Validation:
    - Validates that the HTTP request method is POST, ensuring it only processes POST requests, typically used for form submissions.

    2. Payment Status Handling:
    - Retrieves a payment object from the database based on the invoice ID provided in the POST data.
    - If the payment object is found and the payment status is 'pending', and the action indicates a successful payment ('0' in this case), it updates the payment status to 'successful' in the database. Additional information like the bank message associated with the payment is also saved.

    3. Ticket Generation:
    - Generates tickets for successful payments based on the payment details. Each ticket has a unique series and number, along with other relevant information such as validity and buyer details.
    - Iterates over the number of tickets to be generated, creating a new ticket object for each and saving it to the database.

    4. Email Notification:
    - Constructs an email message to notify the buyer about the successful payment and attaches the generated PDF tickets to the email.
    - Sends the email using Django's email functionality.

    5. Error Handling:
    - Includes exception handling blocks to catch any errors that may occur during the process, such as database errors, ticket generation errors, or email sending errors.
    - If an error occurs, it redirects the user to a failure page and logs the error details for further investigation.
    """
    if request.method == "POST":

        try:
            payment = Payment.objects.get(payment_id=request.POST['invoice_id'])
            # print("Step 2: Successful payment instance fetched for changing status variable! Payment details below")
            # print(f"Payment timestamp is : {payment.timestamp.date()}")
            # print(f"current id is {payment.payment_id} and status: {payment.status}")
            if request.POST['action'] == '0' and payment.status == 'pending':
                payment.status = 'successful'
                payment.bank_message = request.POST['message']
                payment.save()
                
                try:
                    # this must be CHANGED in production...its only to simulate several tickets at once
                    amount = 30
                    tickets =[]
                    for i in range(int(amount/10)):
                        #----------generate new subsequent ticket series and nr
                        ticket_nr = "%06d" % (Ticket.objects.all().count() + 1)
                        ticket_series="DBPNO"
                        ticket_file_name = f"pnb-ticket-{ticket_series}{ticket_nr}.pdf"
                        ticket_id = f"{ticket_series}{ticket_nr}"
                        validity = payment.timestamp.date() + timezone.timedelta(days=90)
                        # create dictionary with all the necessary data for the ticket generator
                        data = {
                                        "qr":ticket_id,
                                        "first_name":payment.buyer_fname,
                                        "last_name":payment.buyer_lname,
                                        "file":ticket_file_name,
                                        "series":ticket_id,
                                        "amount": amount,#in production need to divide by 10
                                        "validity": validity,
                                        'title':"TICHET DE VIZITATOR",
                                        'background_image_path':r"payments/ticket_logos/ticket_bg.png",
                                        "bucegi_logo": r'payments/ticket_logos/bucegi2.png',
                                        "rnp_logo": r'payments/ticket_logos/rnp-romsilva3.png',
                                        "company_name":r'RNP ROMSILVA',
                                        "unit_name":r'ADMINISTRATIA PARCULUI NATURAL BUCEGI R.A.',
                        }

                        
                        # save_pdf_to_location(pdf, "tickets/{}".format(data['file']))
                        #----------save new subsequent ticket in the database
                        try:
                            #======generate pdf ticket for each adult in order and append to list====================
                            tickets.append(generate_pdf_ticket(data))
                            new_ticket = Ticket(
                                            payment_id=payment.payment_id,
                                            buyer_fname=payment.buyer_fname,
                                            buyer_lname=payment.buyer_lname,
                                            ticket_type = "3 luni",
                                            ticket_series=ticket_series,
                                            ticket_nr=ticket_nr,
                                            
                                            )
                            new_ticket.save()
                        except Exception as e:
                            messages.warning(request, f"Ticket creation error! Details:{e}")
                            # attaching the generated pdf ticket
                            return redirect(f'{settings.BASE_URL}/tickets/payment-failure/')
                        
                    try:
                        from django.template.loader import render_to_string
                        from django.utils.html import strip_tags
                        # set email content from html template in /mails/visitor_ticket_email.html with variable buyer names
                        email_body = render_to_string('mails/visitor_ticket_email.html', {'buyer': payment.buyer_fname})
                        # set email data
                        email = EmailMultiAlternatives(
                                            _("Bucegi Natural Park"),
                                            email_body,
                                            settings.EMAIL_HOST_USER,
                                            (f"{payment.email}",),
                                            headers={"Message-ID": settings.TICKET_EMAIL_HEADER,'Content-type': 'text/html'},
                        )
                        # Set the content subtype to HTML
                        email.content_subtype = 'html'
                        # Attach each PDF ticket to the email
                        for i, pdf_ticket in enumerate(tickets, start=1):
                            ticket_name = f'ticket_{i}.pdf'
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(pdf_ticket)
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f'attachment; filename={ticket_name}')
                            email.attach(part)

                        # Send the email
                        email.send()    
                        # email.content_subtype = "html"
                        # email.attach(f"{ticket_id}", pdf, 'application/pdf')
                        # email.send()
                        print(f"successful email delivery")
                        return redirect(f'{settings.BASE_URL}/tickets/payment-success/')
                    except Exception as e:
                        messages.warning(request, f"Application error:{e}")
                        print(f"Cannot send email because:{e}")
                    
                except Exception as e:
                    messages.warning(request, f"Application error:{e}")
                    print(e)
                    return redirect(f'{settings.BASE_URL}/tickets/payment-failure/')
                
            else:
                payment.status = 'failed'
                payment.bank_message = request.POST['message']
                payment.save()
                messages.warning(request, "Payment failed"+f":{payment.bank_message}")
                return redirect(f'{settings.BASE_URL}/tickets/payment-failure/')
        except Exception as e:
            messages.warning(request, f"Application error:{e}. Please contact the administrator at daniel.ungureanu@bucegipark.ro")
            sub_subject = _("To Website Admin: Payment application error")
            from_email='contact@bucegipark.ro'
            sub_message = ''
            html_content=_("Please check payment error with id: {}, connected to email {}.".format(payment.payment_id, payment.email))
            try:
                send_mail(sub_subject, sub_message, from_email, ['daniel.ungureanu@bucegipark.ro'], html_message=html_content)
            except Exception as e:
                messages.warning(request, e)
    else:
        messages.warning(request, f"Application error: No POST data!")
        return redirect(f'{settings.BASE_URL}/tickets/payment-failure/')
        
def check_status_test(request):
    pass
#==============pay_success_view=================
def pay_success_view(request):
    template = "payments/payment-success.html"
    print(request.POST)
    # Store payment_id in session
    request.session['payment_id'] = request.POST['invoice_id']

    messages.success(request, _("Payment successful! Your tickets have been sent to the email you provided. You should always have the tickets with you when visiting Bucegi Natural Park. Thank you!"))
    messages.warning(request, _("If you would like to receive an invoice please press the following button in order to add the necessary info:"))
    context = {

    }
    return render(request, template, context)
#==============ticket invoice view=================
def ticket_invoice(request):
    template = "payments/ticket-invoice.html"
    
    # Retrieve payment_id from session
    # payment = Payment.objects.last() #this method is not the best because if another client does a payment before the previous client finishes sending invoice details we get into trouble
    payment_id = request.session.get('payment_id')
    print(f"Payment is : {payment_id}")

    # Query the Payment object with the retrieved payment_id
    payment = Payment.objects.filter(payment_id=payment_id).first()
    print(payment.price)

    # Check if payment exists before accessing its attributes
    if payment:
        # Query the Ticket objects related to the payment
        tickets = Ticket.objects.filter(payment_id=payment_id)
        #create form instance
        form = CaptchaForm(request.POST)
        
        context = {
            'price': payment.price,
            'quantity': payment.quantity,
            'last_name': payment.buyer_lname,
            'first_name': payment.buyer_fname,
            'phone':payment.phone,
            'email':payment.email,
            'address':payment.address,
            'form': form,
            }
        if request.method == 'POST':
            if form.is_valid():
                from django.template.loader import render_to_string
                from django.utils.html import strip_tags
                fname = request.POST['fname']
                lname = request.POST['fname']
                email = request.POST['email']
                phone = request.POST['phone']
                cnp = request.POST['cnp']

                ticket_series_list = [ticket.ticket_series for ticket in tickets]

                #====send email with invoicing data to bucegipark@gmail.com======
                email_body = render_to_string(
                    'mails/visitor_ticket_email.html', {
                        'buyer_fname': fname,
                        'buyer_lname': lname,
                        'cnp': cnp,
                        'email': email,
                        'phone': phone,
                        'address': payment.address,
                        'series': ticket_series_list,
                        'price': payment.price,
                        'quantity': payment.quantity,
                        })
                email = EmailMultiAlternatives(
                                                _("Factură tichete vizitator"),
                                                email_body,
                                                settings.EMAIL_HOST_USER,
                                                (settings.ACCOUNTANT_EMAIL,),
                                                headers={"Message-ID": settings.TICKET_EMAIL_HEADER,'Content-type': 'text/html'},
                            )
                            # Set the content subtype to HTML
                email.content_subtype = 'html'
                # Clear the session after retrieving payment_id
                request.session.clear()
                messages.success(request, _('The invoicing info has been sent to our financial department and you will receive your invoice in the inbox of the email you provided.'))
                return redirect('checkout')
            else:
                messages.warning(request, _("Failed! Please fill in the captcha field again!"))
                return redirect('home')
        else:
            form = CaptchaForm()
    else:
        # Handle case where payment does not exist
        messages.error(request, _("Payment not found. Please contact support at daniel.ungureanu@bucegipark.ro"))
    return render(request, template, context)
#==============pay_failure_view=================
def pay_failure_view(request):
    template = "payments/payment-failure.html"
    payment = Payment.objects.last()
    if payment:

        messages.warning(request, _(f"Payment failure! Bank message:") + " " + f"{payment.bank_message}")
    else:
        messages.warning(request, _("Payment failure! There is no payment!"))
    context = {
       
    }
    return render(request, template, context)

    
	
    
import hashlib

# --- MONKEY-PATCH FOR cPanel OPENSSL/PYTHON BUILD ---
_original_md5 = hashlib.md5
def _safe_md5(string=b'', *, usedforsecurity=True):
    try:
        return _original_md5(string, usedforsecurity=usedforsecurity)
    except TypeError:
        return _original_md5(string)
hashlib.md5 = _safe_md5

# ---------------------------------------------------
from urllib import request
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import admin
from payments.generate_ticket_pdf2 import generate_pdf_ticket
from .models import Payment, Ticket


@admin.action(description="Regenerate and resend tickets for selected payments")
def resend_tickets(modeladmin, request, queryset):
    success_count = 0
    fail_count = 0

    for payment in queryset:
        if payment.status == 'successful':
            try:
                expiry_str = payment.expiry_date.strftime('%d.%m.%Y') if hasattr(payment, 'expiry_date') and payment.expiry_date else '31.12.2026'

                ticket_data = {
                    'company_name': 'Parcul Natural Bucegi',
                    'unit_name': 'Administrația Ariilor Naturale Protejate',
                    'title': 'Bilet Acces Vizitator',
                    'first_name': payment.buyer_fname,  # Adjust field names to match your Payment model
                    'last_name': payment.buyer_lname,
                    'validity': expiry_str,
                    'qr': f"TICKET-{payment.payment_id}",
                    'background_image_path': settings.BASE_DIR / 'static' / 'images' / 'ticket_bg.png', # Update path if needed
                    'bucegi_logo': settings.BASE_DIR / 'static' / 'images' / 'logo1.png',
                    'rnp_logo': settings.BASE_DIR / 'static' / 'images' / 'logo2.png',
                }
                # generate the PDF ticket
                pdf_bytes = generate_pdf_ticket(ticket_data)

                if not pdf_bytes:
                    raise Exception("PDF generation returned empty content.")

                subject = "Biletul dumneavoastră - Parcul Natural Bucegi"
                body = "Vă mulțumim! Atașat găsiți biletul dumneavoastră de acces actualizat pentru Parcul Natural."
                email = EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [payment.email],
                )
                email.attach(f"bilet_bucegi_{payment.payment_id}.pdf", pdf_bytes, 'application/pdf')
                email.send()

                success_count += 1
            except Exception as e:
                fail_count += 1
                modeladmin.message_user(
                    request, 
                    f"Failed to resend for {payment.payment_id}: {e}", 
                    level='error'
                )
    if success_count > 0:
        modeladmin.message_user(
            request, 
            f"Successfully regenerated and resent tickets for {success_count} payment(s)."
        )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'buyer_fname','buyer_lname', 'status', 'bank_message','quantity', 'price', 'currency', 'phone', 'email', 'address', 'county', 'country', 'city', 'zip', 'notes', ]
    list_display = ('timestamp', 'payment_id', 'status', 'buyer_fname', 'buyer_lname', 'price')
    list_filter = ('status', 'timestamp',)
    search_fields = ('payment_id', 'buyer_fname', 'buyer_lname', 'email')
    actions = [resend_tickets]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ['payment_id','buyer_fname','buyer_lname', 'ticket_series', 'ticket_nr','start_date','expiry_date']
    list_display = ('buyer_fname','buyer_lname', 'ticket_series', 'ticket_nr')


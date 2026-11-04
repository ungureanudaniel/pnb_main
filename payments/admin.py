from urllib import request

from django.contrib import admin
from .models import Payment, Ticket

class PaymentAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'buyer_fname','buyer_lname', 'status', 'bank_message','quantity', 'price', 'currency', 'phone', 'email', 'address', 'county', 'country', 'city', 'zip', 'notes', ]
    list_display = ('timestamp', 'payment_id', 'status', 'buyer_fname', 'buyer_lname', 'price')
class TicketAdmin(admin.ModelAdmin):
    fields = ['payment_id','buyer_fname','buyer_lname', 'ticket_series', 'ticket_nr','start_date','expiry_date']
    list_display = ('buyer_fname','buyer_lname', 'ticket_series', 'ticket_nr')
# class TicketInvoiceAdmin(admin.ModelAdmin):
#     fields = ['', ]
#     list_display = ('',)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Ticket, TicketAdmin)

@admin.action(description="Regenerate and resend tickets for selected payments")
def resend_tickets(modeladmin, request, queryset):
    for payment in queryset:
        if payment.status == 'successful':
            try:
                # Call your ticket generation & email sending function here
                send_tickets_for_payment(payment.payment_id)
                modeladmin.message_user(request, f"Tickets resent successfully for {payment.payment_id}")
            except Exception as e:
                modeladmin.message_user(request, f"Failed to send for {payment.payment_id}: {e}", level='error')
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
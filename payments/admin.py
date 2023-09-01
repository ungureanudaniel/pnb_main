from django.contrib import admin
from .models import Ticket, Payment

class TicketAdmin(admin.ModelAdmin):
    fields = ['buyer_fname', 'buyer_lname', 'ticket_series', 'ticket_nr', 'start_date', 'expiry']

class PaymentAdmin(admin.ModelAdmin):
    fields = ['buyer_fname','buyer_lname', 'payment_id', 'quantity', 'price', 'currency', 'phone', 'email', 'address', 'county', 'country', 'city', 'zip', 'notes', ]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Payment, PaymentAdmin)

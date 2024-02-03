from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import uuid
from django_countries.fields import CountryField
#--------django-payments imports
# from payments import PurchasedItem
# from payments.models import BasePayment

#================Ticket Payment models=====================================
class Payment(models.Model):
    """
    This class creates database tables for each payment made to bucegi natural park administration
    """
    CURRENCY_CHOICES = (
            ('RON', 'RON'),
        )
    STATUS_CHOICES = (
            ('pending', 'pending'),
            ('successful', 'successful'),
            ('failed', 'failed'),
    )
    payment_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField(default=0)
    #if we want kids tickets compulsory then we activate this database column : quantity_kids = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    buyer_fname = models.CharField(max_length=100)
    buyer_lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, blank=False, null=False)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    county = models.CharField(max_length=30)
    country = CountryField(blank_label="Type first letters of your country of residence...")
    city = models.CharField(max_length=30)
    zip = models.CharField(max_length=30)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, default='RON')
    notes = models.TextField(null=True, blank=True)
    bank_message = models.TextField(blank=True, null=True)
    terms = models.BooleanField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default='pending')
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.payment_id}"
#================Ticket models=====================================
class Ticket(models.Model):
    """
    This class creates database tables for each visitor ticket for bucegi natural park
    """
    payment_id = models.CharField(max_length=1000)
    buyer_fname = models.CharField(max_length=100)
    buyer_lname = models.CharField(max_length=100)
    ticket_series =  models.CharField(max_length=5, default="DBPN1")
    ticket_nr = models.CharField(max_length=8)
    start_date = models.DateTimeField(default=timezone.now(), blank=True)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=90), blank=True)
    # ticket_pdf = models.BinaryField()
    ticket_type = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.ticket_series} + {self.ticket_nr}")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.ticket_series} + {self.ticket_nr}"
#================Ticket Invoice models=====================================
# class TicketInvoice(models.Model):
#     """
#     This class creates database tables for each invoice issued for visitor tickets for bucegi natural park
#     """
#     buyer_fname = models.CharField(max_length=100)
#     buyer_lname = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(max_length=254)
#     invoice_description = CharField(max_length=100, blank=False, null=False)
#     price = models.DecimalField(decimal_places=2, max_digits=5)
#     invoice_series =  models.CharField(max_length=3)
#     invoice_nr = models.CharField(max_length=8)
#     slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
#     invoice_date = models.DateTimeField(default=timezone.now(), blank=True)
#     def save(self, *args, **kwargs):
#         self.slug = slugify(f"{self.invoice_series}+{self.invoice_nr}")
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f"{self.invoice_series}" + f"{self.invoice_nr}"
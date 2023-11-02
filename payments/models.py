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
#================Ticket buyer models=====================================
class Ticket(models.Model):
    """
    This class creates database tables for each visitor ticket for bucegi natural park
    """
    buyer_fname = models.CharField(max_length=100)
    buyer_lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    ticket_series =  models.CharField(max_length=3)
    ticket_nr = models.CharField(max_length=8)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
    start_date = models.DateTimeField(default=timezone.now(), blank=True)
    expiry = models.DateTimeField(default=timezone.now() + timedelta(days=90), blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.buyer_fname}+'-'+{self.buyer_lname}")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.buyer_fname}" + " " + f"{self.buyer_lname}"
#================Ticket buyer models=====================================
class Payment(models.Model):
    """
    This class creates database tables for each payment made to bucegi natural park administration
    """
    CURRENCY_CHOICES = (
            ('EUR', 'EUR'),
            ('RON', 'RON'),
        )
    STATUS_CHOICES = (
            ('pending', 'pending'),
            ('successful', 'successful'),
            ('failed', 'failed'),
    )
    payment_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
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
    notes = models.TextField()
    terms = models.BooleanField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default='pending')
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.payment_id}"
#==================payment model from django payments module==============

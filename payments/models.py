from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
#================Ticket buyer models=====================================
# class Ticket(models.Model):
#     """
#     This class creates database tables for each visitor ticket for bucegi natural park
#     """
#     buyer_fname = models.CharField(max_length=100)
#     buyer_lname = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(max_length=254)
#     ticket_series =  models.CharField(max_length=3)
#     ticket_nr = models.CharField(max_length=8)
#     slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
#     start_date = models.DateTimeField(default=now(), blank=True)
#     expiry = models.DateTimeField(default=now() + timedelta(days=90), blank=True)
#     def save(self, *args, **kwargs):
#         self.slug = slugify(f"{self.buyer_fname}+'-'+{self.buyer_lname}")
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f"{self.buyer_fname}" + " " + f"{self.buyer_lname}"
# #================Ticket buyer models=====================================
# class Payment(models.Model):
#     """
#     This class creates database tables for each payment made to bucegi natural park administration
#     """
#     payment_code = models.CharField(max_length=100)
#     sum = models.DecimalField(max_digits=10, decimal_places=3)
#     buyer_fname = models.CharField(max_length=100)
#     buyer_lname = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(max_length=254)
#     address =  models.TextField()
#     county = models.CharField(max_length=30)
#     country = models.CharField(max_length=100)
#     city = models.CharField(max_length=30)
#     zip = models.CharField(max_length=30)
#     notes = models.TextField()
#     slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.payment_code)
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f"{self.buyer_fname}" + " " + f"{self.buyer_lname}"

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
#================Ticket buyer models=====================================
class Ticket(models.Model):
    """
    This class creates database tables for each visitor ticket for bucegi natural park
    """
    buyer_fname = models.CharField(max_length=100)
    buyer_lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    group_persons = models.TextField()
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
    timestamp = models.DateTimeField(default=now(), blank=True)
    expiry = models.DateTimeField(default=now() + timedelta(days=90), blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.buyer_fname}" + " " + f"{self.buyer_lname}"

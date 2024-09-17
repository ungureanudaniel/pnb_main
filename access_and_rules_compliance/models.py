from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class LawCategory(models.Model):
    """
    This class creates database tables for categories for each law documents
    category for natural park bucegi administration
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Legislation category'
        verbose_name_plural = "Legislation category"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
#===============legislation model==================================
class Law(models.Model):
    """
    This class creates database tables for categories for each law documents
    for natural park bucegi administration
    """
    LANG_CHOICE = (
            (_('English'), _('English')),
            (_('Romanian'), _('Romanian')),
        )
    title = models.CharField(max_length=500)
    text = models.TextField()
    doc_type = models.CharField(max_length=100)
    doc_nr = models.CharField(max_length=10)
    publish_date = models.DateField(default=timezone.now)
    category = models.ForeignKey(LawCategory, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default='Romanian', choices=LANG_CHOICE)
    link = models.FileField(upload_to='public_docs/legislation/%d_%b_%Y/', max_length=300, blank =True, null=True)
    slug = models.SlugField(allow_unicode=True, max_length=500, blank=True, editable=False)

    class Meta:
        verbose_name = 'Law'
        verbose_name_plural = "Laws"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
    

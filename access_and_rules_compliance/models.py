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
        verbose_name = 'Law Document'
        verbose_name_plural = "Law Documents"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
class Law(models.Model):
    """
    This class creates database tables for categories for each law documents
    for natural park bucegi administration
    """
    LANG_CHOICE = (
            (_('English'), _('English')),
            (_('Romanian'), _('Romanian')),
        )
    title = models.CharField(max_length=200)
    text = models.TextField()
    publish_date = models.DateField(default=timezone.now)
    category = models.ForeignKey(LawCategory, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default='Romanian', choices=LANG_CHOICE)

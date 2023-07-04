from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone
import os
from django.contrib.auth.models import User
#blog imports
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
#================Announcement models=====================================
class Announcement(models.Model):
    """
    This class creates database tables for each announcement of bucegi natural park
    """
    title = models.CharField(max_length=100)
    image = ResizedImageField(size=[640,None], upload_to='announcement_images',)
    text = RichTextField()
    link_ro = models.FileField(upload_to='announcements/%d_%b_%Y/', max_length=254, blank =True, null=True)
    link_en = models.FileField(upload_to='announcements/%d_%b_%Y/', max_length=254, blank =True, null=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now, blank=True)
    expiry = models.DateTimeField(blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    # @property
    # def relative_path(self):
    #     return os.path.relpath(self.path, settings.MEDIA_ROOT)
    def __str__(self):
        return self.title
#================Partners models=====================================
class Partner(models.Model):
    """
    This class creates database tables for each partner of bucegi natural park
    """
    title = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='partner_images',)
    link = models.URLField(max_length = 300)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
    rank = models.IntegerField()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
#================Events models=====================================
class Event(models.Model):
    """
    This class creates database tables for each event in bucegi natural park
    """
    title = models.CharField(max_length=30)
    text = RichTextField(max_length=3000)
    image = ResizedImageField(size=[640,None], upload_to='event_images',)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    expiry = models.DateTimeField(default=timezone.now, blank=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        ordering = ["-timestamp"]
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
#================Public docs models=====================================
class PublicCategory(models.Model):
    """
    This class creates database tables for categories for each public documents
    category for natural park bucegi administration
    """
    title = models.CharField(max_length=70)
    text = RichTextField()
    # link_ro = models.FileField(upload_to='public_docs/%d_%b_%Y/', max_length=254, blank =True, null=True)
    # link_en = models.FileField(upload_to='public_docs/%d_%b_%Y/', max_length=254, blank =True, null=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Public Document'
        verbose_name_plural = "Public Documents"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
#================Public docs models=====================================
class PublicCatLink(models.Model):
    """
    This class creates database tables for download links per years for each publi
    documents category
    """
    year = models.CharField(max_length=4)
    category = models.ForeignKey(PublicCategory, on_delete=models.CASCADE)
    link_ro = models.FileField(upload_to='public_docs/%d_%b_%Y/', max_length=300, blank =True, null=True)
    link_en = models.FileField(upload_to='public_docs/%d_%b_%Y/', max_length=300, blank =True, null=True)

    class Meta:
        verbose_name = 'Public Documents Link'
        verbose_name_plural = "Public Documents Links"
        ordering = ["-year"]

    def __str__(self):
        return self.year
#================Council docs Category models=====================================
class CouncilDocsCategory(models.Model):
    """
    This class creates database tables for categories for each council documents
    category for natural park bucegi administration
    """
    title = models.CharField(max_length=70)
    text = RichTextField()
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Council Document'
        verbose_name_plural = "Council Documents"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
#================Council docs links models=====================================
class CouncilCatLink(models.Model):
    """
    This class creates database tables for download links per years for each council
    documents category, linked by foreignkey to CouncilDocsCategory
    """
    year = models.CharField(max_length=4)
    category = models.ForeignKey(CouncilDocsCategory, on_delete=models.CASCADE)
    link = models.FileField(upload_to='public_docs/%d_%b_%Y/', max_length=300, blank =True, null=True)

    class Meta:
        verbose_name = 'Council Documents Link'
        verbose_name_plural = "Council Documents Links"
        ordering = ["-year"]

    def __str__(self):
        return self.year
#================testimonial model=====================================
class Testimonial(models.Model):
    """
    This class creates database tables for each testimonial given on the page of
     Natural park bucegi
    """
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    thumbnail = ResizedImageField(size=[640,None], upload_to='testimonial_images',)
    text = models.TextField(max_length=300)
    status = models.BooleanField(default="False")
    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = "Testimonials"
    def __str__(self):
        return self.email
#================Attraction category models=====================================
class AttractionCategory(models.Model):
    """
    This class creates database tables for categories for each attraction in
    natural park bucegi
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Attraction Category'
        verbose_name_plural = "Attraction Categories"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
#================Attraction model=====================================
class Attraction(models.Model):
    """
    This class creates database tables for each attraction in natural park bucegipark
    linked to attraction category table above, by ForeignKey. The images for attraction
    will be automatically resized using a package : django-resized. Default settings in
    settings.py file.
    """
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='attraction_images',)
    text = models.TextField(max_length=2000)
    categ = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
#================Flora category models=====================================
class FloraCategory(models.Model):
    """
    This class creates database tables for categories for each flora species in
    natural park bucegi
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Flora Category'
        verbose_name_plural = "Flora Categories"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug

#================Wildlife category models=====================================
class WildlifeCategory(models.Model):
    """
    This class creates database tables for categories for each wildlife species in
    natural park bucegi
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Wildlife Category'
        verbose_name_plural = "Wildlife Categories"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.slug
#================Flora models=====================================
class Flora(models.Model):
    """
    This class creates database tables for each flora species in natural park bucegipark
    linked to flora categories table above, by ForeignKey. The images for flora
    will be automatically resized using a package : django-resized. Default settings in
    settings.py file.
    """
    CONS_STATUS = (
            (_('Endagered'), _('Endagered')),
            (_('Data Deficient'), _('Data Deficient')),
            (_('Least Concern'), _('Least Concern')),
            (_('Near Threatened'), _('Near Threatened')),
            (_('Vulnerable'), _('Vulnerable')),
            (_('Critically Endangered'), _('Critically Endangered')),
            (_('Extinct In The Wild'), _('Extinct In The Wild')),
            (_('Extinct'), _('Extinct')),
        )
    MONTHS = (
            (_('January'), _('January')),
            (_('February'), _('February')),
            (_('March'), _('March')),
            (_('April'), _('April')),
            (_('May'), _('May')),
            (_('June'), _('June')),
            (_('July'), _('July')),
            (_('August'), _('August')),
            (_('September'), _('September')),
            (_('October'), _('October')),
            (_('November'), _('November')),
            (_('December'), _('December')),

        )
    FLOWER_LIFE = (
            (_('Annual'), _('Annual')),
            (_('Perennial'), _('Perennial')),
            (_('Biennial'), _('Biennial')),
        )
    name = models.CharField(max_length=30)
    image = image = models.ImageField(upload_to='flora_image', blank=True)
    text = models.TextField(max_length=2000)
    height_max = models.IntegerField()
    flowering_start = models.CharField(max_length=30, default='April', choices=MONTHS)
    flowering_end = models.CharField(max_length=30, default='September', choices=MONTHS)
    cons_status = models.CharField(max_length=30, default='Least Concern', choices=CONS_STATUS)
    life_span = models.CharField(max_length=30, default='Annual', choices=FLOWER_LIFE)
    habitat = models.TextField(max_length=1000)
    categ = models.ForeignKey(FloraCategory, on_delete=models.CASCADE)
    family = models.CharField(max_length=100, default="flora", editable=False)
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Flora species'
        verbose_name_plural = "Flora species"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

#================Wildlife model=====================================
class Wildlife(models.Model):
    """
    This class creates database tables for each wildlife species in natural park bucegipark
    linked to wildlife category table above, by ForeignKey. The images for wildlife
    will be automatically resized using a package : django-resized. Default settings in
    settings.py file.
    """
    CONS_STATUS = (
        (_('Endagered'), _('Endagered')),
        (_('Data Deficient'), _('Data Deficient')),
        (_('Least Concern'), _('Least Concern')),
        (_('Near Threatened'), _('Near Threatened')),
        (_('Vulnerable'), _('Vulnerable')),
        (_('Critically Endangered'), _('Critically Endangered')),
        (_('Extinct In The Wild'), _('Extinct In The Wild')),
        (_('Extinct'), _('Extinct')),
    )
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='wildlife_image', blank=True)
    text = models.TextField(max_length=2000)
    # weight_min = models.IntegerField()
    # weight_max = models.IntegerField()
    # weight_min = models.DecimalField(max_digits=None, decimal_places=3)
    # weight_max = models.DecimalField(max_digits=None, decimal_places=3)
    cons_status = models.CharField(max_length=30, default='Least Concern', choices=CONS_STATUS)
    life_span_max = models.IntegerField()
    habitat = models.TextField(max_length=1000)
    diet = models.CharField(max_length=300)
    categ = models.ForeignKey(WildlifeCategory, on_delete=models.CASCADE)
    family = models.CharField(max_length=100, default="wildlife", editable=False)
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Wildlife species'
        verbose_name_plural = "Wildlife species"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
#================Gallery model=====================================
# class Gallery(models.Model):
#     """
#     This class creates database tables for each photo in natural park bucegipark
#     linked to attraction category table above, by ForeignKey. The images for attraction
#     will be automatically resized using a package : django-resized. Default settings in
#     settings.py file.
#     """
#     name = models.CharField(max_length=30)
#     image = ResizedImageField(size=[640,None], upload_to='gallery_images',)
#     text = models.TextField(max_length=300)
#     categ = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE)
#     slug = models.SlugField(max_length=100, blank=True, null=True)
#     featured = models.BooleanField(default=False)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.slug
#================Team model=====================================
class Team(models.Model):
    """
    This class creates database tables for each team member of natural park. The
    images for each member will be automatically resized using a package : django-resized.

    """
    COUNTY = (
        ('Brașov', 'Brașov'),
        ('Dâmbovița', 'Dâmbovița'),
        ('Prahova', 'Prahova'),
    )
    # AREA = (
    #     ('Azuga', 'Azuga'),
    #     ('Dâmbovița', 'Dâmbovița'),
    #     ('Prahova', 'Prahova'),
    # )
    surname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='team_images',)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    judet = models.CharField(max_length=10, default='Draft', choices=COUNTY)
    job = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=300)
    hierarchy = models.IntegerField(default=0)
    sector = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.surname}" + " " + f"{self.firstname}"

#================Scientific council model=====================================
class SCouncil(models.Model):
    """
    This class creates database tables for each scientific council member of Bucegi natural park. The
    images will be automatically resized using a package : django-resized.

    """
    title = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='scouncil_images',)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254)
    cv = models.FileField(upload_to='scouncil/', max_length=254, blank =True, null=True)
    interest = models.CharField(max_length=200)
    hierarchy = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Scientific Council Member')
        verbose_name_plural = _("Scientific Council Members")

    def __str__(self):
        return f"{self.surname}" + " " + f"{self.firstname}"
    
#================contact model=====================================
class Contact(models.Model):
    """
    This class creates database tables for each contact message send from contact page of
     Natural park bucegi
    """
    author = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=50)
    text = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = "Contact"
    def __str__(self):
        return '{}'.format(self.email)
#================subscribers model=====================================
class Subscriber(models.Model):
    email = models.EmailField(max_length=200)
    conf_num =  models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
#----------------------------------THE CATEGORY MODEL-------------------------
class BlogPostCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Blog Post Category"
        verbose_name_plural = "Blog Post Categories"

    def __str__(self):
        return '{}'.format(self.title)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(BlogPostCategory, self).save(*args, **kwargs)
#----------------------------------THE POST MODEL----------------------------
class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_image', blank=True)
    text = RichTextField(blank=True, null=True)
    category = models.ForeignKey(BlogPostCategory, on_delete=models.CASCADE, related_name='postcategory')
    featured = models.BooleanField()
    slug = models.SlugField(max_length=255, editable=False)
    created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    status = models.CharField(max_length=10, default='Draft', choices=STATUS_CHOICES)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ["-created_date"]

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug

#----------------------PARK RULES MODEL--------------------------------------------
class ParkRules(models.Model):
    name = models.CharField(max_length=255)
    text=RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
#----------------------COMMENTS MODEL--------------------------------------------
class Comment(models.Model):
    thumbnail = models.ImageField(upload_to='comments')
    name = models.CharField(max_length=255)
    text=models.TextField(null=True)
    post=models.ForeignKey(BlogPost,related_name="post",null=True,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth.models import User
#blog imports
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

#================Partners models=====================================
class Announcement(models.Model):
    """
    This class creates database tables for each announcement of bucegi natural park
    """
    title = models.CharField(max_length=100)
    text = RichTextField(max_length=3000)
    link_ro = models.FileField(upload_to='announcements/%d %b %Y/', max_length=254, blank =True, null=True)
    link_en = models.FileField(upload_to='announcements/%d %b %Y/', max_length=254, blank =True, null=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
#================Partners models=====================================
class Partner(models.Model):
    """
    This class creates database tables for each partner of bucegi natural park
    """
    title = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='partner_images',)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

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
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        ordering = ["-date"]
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
    title = models.CharField(max_length=30)
    text = RichTextField(max_length=3000)
    link_ro = models.FileField(upload_to='public_docs/%d %b %Y/', max_length=254, blank =True, null=True)
    link_en = models.FileField(upload_to='public_docs/%d %b %Y/', max_length=254, blank =True, null=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Public Document'
        verbose_name_plural = "Public Documents"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
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
    image = ResizedImageField(size=[640,None], upload_to='attraction_images',)
    text = models.TextField(max_length=300)
    categ = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
#================Gallery model=====================================
class Gallery(models.Model):
    """
    This class creates database tables for each photo in natural park bucegipark
    linked to attraction category table above, by ForeignKey. The images for attraction
    will be automatically resized using a package : django-resized. Default settings in
    settings.py file.
    """
    name = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='gallery_images',)
    text = models.TextField(max_length=300)
    categ = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug
#================Team model=====================================
class Team(models.Model):
    """
    This class creates database tables for each team member of natural park. The
    images for attraction will be automatically resized using a package : django-resized.

    """
    surname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    image = ResizedImageField(size=[640,None], upload_to='team_images',)
    phone = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=300)
    hierarchy = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = "Team Members"

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
#----------------------COMMENTS MODEL--------------------------------------------
class Comment(models.Model):
    thumbnail = models.ImageField(upload_to='comments')
    name = models.CharField(max_length=255)
    text=models.TextField(null=True)
    post=models.ForeignKey(BlogPost,related_name="post",null=True,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

from django.contrib import admin
from .models import Testimonial, Team, AttractionCategory, Contact,\
PublicCategory, Attraction, Subscriber, BlogPost, BlogPostCategory, Event,\
Partner, Comment, Announcement, PublicCatLink

class AttractionCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_en', 'name_ro', 'name_de']


class AttractionAdmin(admin.ModelAdmin):
    fields = ['name', 'name_en', 'name_ro', 'name_de', 'image', 'text', 'text_en', 'text_ro', 'text_de', 'categ']
    prepopulated_fields = {"name":("name_en",),"text":("text_en",)}

class TestimonialAdmin(admin.ModelAdmin):
    fields = ['status', 'fname', 'lname', 'email', 'thumbnail', 'text']

class PartnerAdmin(admin.ModelAdmin):
    fields = ['title', 'image']

class TeamAdmin(admin.ModelAdmin):
    fields = ['firstname', 'surname', 'image', 'text', 'phone', 'job','job_ro', 'job_de', 'job_en', 'hierarchy']

class ContactAdmin(admin.ModelAdmin):
    fields = ['subject', 'author', 'email']
class PublicCatLinkAdmin(admin.ModelAdmin):
    list_display = ('year', 'category', 'link_ro', 'link_en')
    fields = ['year', 'category', 'link_ro', 'link_en']
class PublicCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_en')
    fields = ['title', 'title_en', 'title_ro', 'title_de', 'text', 'text_en', 'text_ro', 'text_de']
class AnnouncementAdmin(admin.ModelAdmin):
    fields = ['title', 'title_en', 'title_ro', 'title_de', 'text', 'text_en', 'text_ro', 'text_de', 'link_en', 'link_ro']
class CommentAdmin(admin.ModelAdmin):
    fields = ['name', 'text', 'thumbnail', 'active']
class EventAdmin(admin.ModelAdmin):
    fields = ['title_en', 'title_ro', 'title_de', 'title', 'text_en', 'text_ro', 'text_de', 'text', 'image', 'date']
    prepopulated_fields = {"title": ("title_en",), "text": ("text_en",)}

class SubscriberAdmin(admin.ModelAdmin):
    fields = ['email', 'conf_num', 'confirmed']

class BlogPostCategoryAdmin(admin.ModelAdmin):
    fields = ['title_en', 'title_ro', 'title_de']
    # prepopulated_fields = {"slug": ("title_en",)}
class BlogPostAdmin(admin.ModelAdmin):
    fields = ['author', 'title_en', 'title_ro', 'title_de', 'title', 'image', 'text_en', 'text_ro', 'text_de', 'text', 'category', 'featured', 'status']
    prepopulated_fields = {"title": ("title_en",), "text": ("text_en",)}

admin.site.register(Comment, CommentAdmin)
admin.site.register(PublicCatLink, PublicCatLinkAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(PublicCategory, PublicCategoryAdmin)
admin.site.register(Attraction, AttractionAdmin)
admin.site.register(AttractionCategory, AttractionCategoryAdmin)

from django.contrib import admin
from .models import Testimonial, Team, AttractionCategory, Contact,\
PublicCategory, Attraction, Subscriber, BlogPost, BlogPostCategory, Event,\
Partner, Comment, Announcement, PublicCatLink, FloraCategory, WildlifeCategory,\
Flora, SCouncil, PublicDocsDownloaderEntity, MngPlanDocsCategory, MngPlanCatLink,\
ParkRegulationCategory, ParkRegulationCatLink,\
Wildlife
class AttractionCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_ro', 'name_de']

class AttractionAdmin(admin.ModelAdmin):
    fields = ['categ','name', 'name_ro', 'name_de', 'image', 'text', 'text_ro', 'text_de', 'featured']
    list_display = ('name', 'categ', 'image', 'featured')
class WildlifeCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_ro', 'name_de']

class FloraCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_ro', 'name_de']

class FloraAdmin(admin.ModelAdmin):
    fields = [ 'categ', 'name', 'name_ro', 'name_de', 'image', 'height_max', 'flowering_start', 'flowering_end', 'habitat', 'habitat_ro', 'habitat_de', 'cons_status', 'life_span', 'text', 'text_ro', 'text_de', 'featured']
class WildlifeAdmin(admin.ModelAdmin):
    fields = [ 'categ', 'name', 'name_ro', 'name_de', 'image', 'height_max', 'weight_max', 'life_span_max', 'habitat', 'habitat_ro', 'habitat_de', 'diet', 'diet_ro', 'diet_de', 'cons_status', 'text', 'text_ro', 'text_de', 'featured']

class TestimonialAdmin(admin.ModelAdmin):
    fields = ['status', 'fname', 'lname', 'email', 'thumbnail', 'text']

class PartnerAdmin(admin.ModelAdmin):
    fields = ['title','link', 'image','rank']

class TeamAdmin(admin.ModelAdmin):
    fields = ['firstname', 'surname', 'image', 'text', 'phone', 'email', 'job','job_ro', 'job_de', 'judet', 'sector', 'sector_ro', 'sector_de', 'hierarchy']

class ContactAdmin(admin.ModelAdmin):
    fields = ['subject', 'author', 'email']
class PublicCatLinkAdmin(admin.ModelAdmin):
    list_display = ('year', 'category', 'link_ro', 'link_en')
    fields = ['year', 'category', 'link_ro', 'link_en']
class PublicCategoryAdmin(admin.ModelAdmin):
    list_display = ('title_en',)
    fields = ['title', 'title_ro', 'title_de', 'text', 'text_ro', 'text_de']
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'expiry')
    fields = ['title', 'title_ro', 'title_de','timestamp','expiry', 'image', 'text', 'text_ro', 'text_de', 'link_en', 'link_ro']
class CommentAdmin(admin.ModelAdmin):
    fields = ['name', 'text', 'thumbnail', 'active']
class EventAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'expiry', 'title', 'title_ro', 'title_de',  'text', 'text_ro', 'text_de', 'image']
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'conf_num', 'confirmed')
    fields = ['email', 'conf_num', 'confirmed']
class BlogPostCategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'title_ro', 'title_de']
class BlogPostAdmin(admin.ModelAdmin):
    fields = ['author', 'created_date', 'title', 'title_ro', 'title_de', 'image', 'text', 'text_ro', 'text_de', 'category', 'featured', 'status']
class SCouncilAdmin(admin.ModelAdmin):
    fields = ['title', 'firstname', 'surname', 'image', 'cv', 'interest', 'interest_ro', 'interest_de', 'phone', 'email', 'hierarchy']
class PublicDocsDownloaderEntityAdmin(admin.ModelAdmin):
    fields = ['institution', 'name', 'email']
    list_display = ('institution', 'name', 'email')
# class CouncilDocsCategoryAdmin(admin.ModelAdmin):
#     list_display = ('title',)
#     fields = ['title', 'text',]
# class CouncilCatLinkAdmin(admin.ModelAdmin):
#     list_display = ('year', 'category', 'link')
#     fields = ['year', 'category', 'link']
class MngPlanDocsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ['title', 'title_ro', 'title_de', 'text', 'text_ro', 'text_de']
class MngPlanCatLinkAdmin(admin.ModelAdmin):
    list_display = ('year', 'category', 'link')
    fields = ['year', 'category', 'link']
class ParkRegulationCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ['title', 'title_ro', 'title_de', 'text', 'text_ro', 'text_de']
class ParkRegulationCatLinkAdmin(admin.ModelAdmin):
    list_display = ('year', 'category', 'link')
    fields = ['year', 'category', 'link']
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
admin.site.register(Flora, FloraAdmin)
admin.site.register(Wildlife, WildlifeAdmin)
admin.site.register(FloraCategory, FloraCategoryAdmin)
admin.site.register(WildlifeCategory, WildlifeCategoryAdmin)
admin.site.register(SCouncil, SCouncilAdmin)
# admin.site.register(CouncilCatLink, CouncilCatLinkAdmin)
# admin.site.register(CouncilDocsCategory, CouncilDocsCategoryAdmin)
admin.site.register(PublicDocsDownloaderEntity, PublicDocsDownloaderEntityAdmin)
admin.site.register(MngPlanCatLink, MngPlanCatLinkAdmin)
admin.site.register(MngPlanDocsCategory, MngPlanDocsCategoryAdmin)
admin.site.register(ParkRegulationCatLink, ParkRegulationCatLinkAdmin)
admin.site.register(ParkRegulationCategory, ParkRegulationCategoryAdmin)
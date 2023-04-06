from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import BlogPost, AttractionCategory, Event, Team

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return BlogPost.objects.all()
    def location(self,obj):
        return '/%s' % (obj.title)

class AttractionCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return AttractionCategory.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)

class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Event.objects.all()
    def location(self,obj):
        return '/%s' % (obj.title)

class TeamSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Team.objects.all()
    def location(self,obj):
        return '/%s' % (obj.job)

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['home', 'team', 'wildlife', 'contact']

    def location(self, item):
        return reverse(item)

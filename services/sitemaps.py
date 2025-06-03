from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import AttractionCategory, Event, Team, FloraCategory, Flora,\
WildlifeCategory, Wildlife


class AttractionCategorySitemap(Sitemap):
    """Sitemap for attraction categories."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return AttractionCategory.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)


class FloraCategorySitemap(Sitemap):
    """Sitemap for flora categories."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return FloraCategory.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)


class FloraSitemap(Sitemap):
    """Sitemap for flora."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Flora.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)


class WildlifeSitemap(Sitemap):
    """Sitemap for wildlife."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Wildlife.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)


class WildlifeCategorySitemap(Sitemap):
    """Sitemap for wildlife categories."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return WildlifeCategory.objects.all()
    def location(self,obj):
        return '/%s' % (obj.name)


class EventSitemap(Sitemap):
    """Sitemap for events."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Event.objects.all()
    def location(self,obj):
        return '/%s' % (obj.title)


class TeamSitemap(Sitemap):
    """Sitemap for team members."""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Team.objects.all()
    def location(self,obj):
        return '/%s' % (obj.job)


class StaticViewSitemap(Sitemap):
    """Sitemap for static views."""
    changefreq = 'monthly'

    def items(self):
        return ['home', 'team', 'wildlife', 'flora', 'events', 'contact']

    def location(self, item):
        return reverse(item)

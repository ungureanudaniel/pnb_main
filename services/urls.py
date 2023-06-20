from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from .views import home, contacts_view, coming_soon, gallery, team, history,\
wildlife, flora, faq_view, theme_trails, video_view, public_docs,\
add_testimonial, ticket_info, bloglist_view, privacy_view, PostDetailView,\
blogsearch_view, eventlist_view, map_coming_soon, terms_view, infopoints_view,\
announcement_view, AnnounDetailView, WildlifeDetailView, FloraDetailView, subscription_conf_view,\
unsubscribe, sector_map_view, page_not_found, server_error, park_rules,council_view
from django.conf.urls.static import static
from users.views import user_logout
from django.utils.translation import gettext_lazy as _

urlpatterns = [
        #-------Authentication----------------
        path('logout/', user_logout, name='signout'),
        #-------Visitor urls------------------
        path(_('home'), home, name="home"),
        path('contact', contacts_view, name="contact"),
        path('coming-soon', coming_soon, name="coming-soon"),
        path(_('gallery'), gallery, name="gallery"),
        path(_('team'), team, name="team"),
        path(_('wildlife'), wildlife, name="wildlife"),
        path(_('flora'), flora, name="flora"),
        path(_('history'), history, name="history"),
        path(_('videos'), video_view, name="videos"),
        path(_('frequently-asked-questions'), faq_view, name="faq"),
        path(_('theme-trails'), theme_trails, name="theme-trails"),
        path(_('public-documents'), public_docs, name="public-docs"),
        path(_('ticket-information'), ticket_info, name="ticket-info"),
        path(_('privacy_information'), privacy_view, name="privacy_info"),
        path(_('terms-conditions'), terms_view, name="terms"),
        path(_('info-points'), infopoints_view, name="infopoints"),
        path(_('announcements'), announcement_view, name="announcement"),
        path(_('announcements/<slug:slug>/'), AnnounDetailView.as_view(), name='announ-details'),
        path(_('wildlife-info/<slug:slug>/'), WildlifeDetailView.as_view(), name='wildlife-details'),
        path(_('flora-info/<slug:slug>/'), FloraDetailView.as_view(), name='flora-details'),
        path(_('subscription-confirmation/'), subscription_conf_view, name='subscription-confirmation'),
        path(_('unsubscribe'), unsubscribe, name='unsubscribe'),
        path(_('scientific-council'), council_view, name='scientific-council'),

        #------------map urls-------------------------------
        path('park-map', map_coming_soon, name="map_coming_soon"),
        path('park-sectors', sector_map_view, name="sector-map"),
        path('park-rules', park_rules, name="park-rules"),
        #------------blog urls------------------------------
        path('blog', bloglist_view, name="blog"),
        path('blog/<slug:slug>/', PostDetailView.as_view(), name='blog-details'),
        path('blog-search/q/', blogsearch_view, name="blogsearch"),
        #--------events urls-----------------------------
        path(_('events'), eventlist_view, name="events"),

        #---------add content urls---------------------
        path('add-testimonial', add_testimonial, name="add_testimonial"),



    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

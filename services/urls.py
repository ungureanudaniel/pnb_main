from django.urls import path, include
from django.conf import settings
from .views import home, contacts_view, coming_soon, gallery, team, history,\
flora, faq_view, theme_trails, video_view, public_docs,\
add_testimonial, ticket_info, bloglist_view, privacy_view, PostDetailView,\
blogsearch_view, eventlist_view, map_coming_soon, terms_view, infopoints_view,\
announcement_view, AnnounDetailView, FloraDetailView, subscription_conf_view,\
unsubscribe, sector_map_view, council_view, mng_plan_view, allowed_vehicles,\
park_regulation_view, WildlifeDetailView, wildlife, EventDetailView, ArticleMonthArchiveView
from django.conf.urls.static import static
from users.views import user_logout
from django.utils.translation import gettext_lazy as _

urlpatterns = [
        #-------Authentication----------------
        path('logout/', user_logout, name='signout'),
        #-------Visitor urls------------------
        path('', home, name="home"),
        path('contact', contacts_view, name="contact"),
        path('coming-soon', coming_soon, name="coming-soon"),
        path('gallery', gallery, name="gallery"),
        path('team', team, name="team"),
        path('wildlife', wildlife, name="wildlife"),
        path('flora', flora, name="flora"),
        path('history', history, name="history"),
        path('videos', video_view, name="videos"),
        path('frequently-asked-questions', faq_view, name="faq"),
        path('theme-trails', theme_trails, name="theme-trails"),
        path('ticket-information', ticket_info, name="ticket-info"),
        path('privacy_information', privacy_view, name="privacy_info"),
        path('terms-conditions', terms_view, name="terms"),
        path('info-points', infopoints_view, name="infopoints"),
        path('announcements', announcement_view, name="announcement"),
        path('<int:year>/<str:month>/', ArticleMonthArchiveView.as_view(), name="announcements_archive"),
        path('announcements/<slug:slug>/', AnnounDetailView.as_view(), name='announ-details'),
        path('wildlife-info/<slug:slug>/', WildlifeDetailView.as_view(), name='wildlife-details'),
        path('flora-info/<slug:slug>/', FloraDetailView.as_view(), name='flora-details'),
        path('event-details/<slug:slug>/', EventDetailView.as_view(), name='event-details'),
        path('subscription-confirmation/', subscription_conf_view, name='subscription-confirmation'),
        path('unsubscribe', unsubscribe, name='unsubscribe'),
        path('scientific-council', council_view, name='scientific-council'),
        #--------------public documents---------------------
        path('park-rules', park_regulation_view, name="park-rules"),
        path('public-documents', public_docs, name="public-docs"),
        path('management-plan', mng_plan_view, name="mng-plan"),
        path('allowed-vehicles', allowed_vehicles, name="auto-access"),
        #------------map urls-------------------------------
        path('park-map', map_coming_soon, name="map_coming_soon"),
        path('park-sectors', sector_map_view, name="sector-map"),
        #------------blog urls------------------------------
        path('blog', bloglist_view, name="blog"),
        path('blog/<slug:slug>/', PostDetailView.as_view(), name='blog-details'),
        path('blog-search/q/', blogsearch_view, name="blogsearch"),
        #--------events urls-----------------------------
        path('events', eventlist_view, name="events"),
        #---------add content urls---------------------
        path('add-testimonial', add_testimonial, name="add_testimonial"),



    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

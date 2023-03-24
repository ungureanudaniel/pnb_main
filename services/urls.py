from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView
from .views import home, contacts_view, coming_soon, gallery, team, history,\
wildlife, flora, invalid_header, faq_view, theme_trails, video_view, public_docs,\
add_testimonial, ticket_info, bloglist_view, privacy_view, PostDetailView,\
blogsearch_view, eventlist_view, map_coming_soon, terms_view, infopoints_view
from django.conf.urls.static import static
from users.views import user_logout

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
        path('_(frequently-asked-questions)', faq_view, name="faq"),
        path('theme-trails', theme_trails, name="theme-trails"),
        path('public-documents', public_docs, name="public-docs"),
        path('ticket-information', ticket_info, name="ticket-info"),
        path('privacy_information', privacy_view, name="privacy_info"),
        path('terms-conditions', terms_view, name="terms"),
        path('info-points', infopoints_view, name="infopoints"),


        #------------map urls-------------------------------
        path('park-map', map_coming_soon, name="map_coming_soon"),
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

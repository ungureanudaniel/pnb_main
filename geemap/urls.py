from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import map_view

urlpatterns = [
    #------ general urls-------------------
    path('map/', map_view, name='map'),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

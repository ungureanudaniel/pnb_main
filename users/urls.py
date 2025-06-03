from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view


urlpatterns = [
    #------ general urls-------------------
    path('login/', login_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

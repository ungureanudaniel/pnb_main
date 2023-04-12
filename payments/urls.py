from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ticketpay

urlpatterns = [
    #------ general urls-------------------
    path('visitor-ticket-payment', ticketpay, name="ticketpay"),
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

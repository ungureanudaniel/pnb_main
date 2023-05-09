from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ticketpay_view, checkout_view

urlpatterns = [
    #------ general urls-------------------
    path('online-ticket-details', ticketpay_view, name="ticket-online"),
    path('payment-checkout', checkout_view, name="checkout"),

    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

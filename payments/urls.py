from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import choosetickets_view, checkout_view, pay_success_view, pay_failure_view

urlpatterns = [
    #------ general urls-------------------
    path('choose-tickets', choosetickets_view, name="choose-tickets"),
    path('payment-checkout', checkout_view, name="checkout"),
    path('payment-success', pay_success_view, name="pay-success"),
    path('payment-failure', pay_failure_view, name="pay-failure"),

    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

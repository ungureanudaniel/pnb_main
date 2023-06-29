from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import choosetickets_view, checkout_view, pay_confirm_view, pay_return_view

urlpatterns = [
    #------ general urls-------------------
    path('choose-tickets', choosetickets_view, name="choose-tickets"),
    path('payment-checkout', checkout_view, name="checkout"),
    path('payment-confirmation', pay_confirm_view, name="pay-confirm"),
    path('payment-return', pay_return_view, name="pay-return"),

    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from .views import checkout_view, pay_success_view, pay_failure_view, check_status

urlpatterns = [
    #------ general urls-------------------
    # path('choose-tickets', choosetickets_view, name="choose-tickets"),
    path('payment-checkout/', csrf_exempt(checkout_view), name="checkout"),
    path('payment-success/', csrf_exempt(pay_success_view), name="pay-success"),
    path('payment-failure/', csrf_exempt(pay_failure_view), name="pay-failure"),
    path('status/', csrf_exempt(check_status), name='status'),


    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

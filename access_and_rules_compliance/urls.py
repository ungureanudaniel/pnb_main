from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import allowed_vehicles, laws, search_laws, single_vehicle_upload, bulk_vehicle_upload,\
      registered_vehicles_list

urlpatterns = [
    #------ general urls-------------------
    # path('choose-tickets', choosetickets_view, name="choose-tickets"),
    path('allowed-vehicles/', allowed_vehicles, name="auto-access"),
    path('vehicle/add/', single_vehicle_upload, name='single_vehicle_upload'),
    path('vehicle/bulk-upload/', bulk_vehicle_upload, name='bulk_vehicle_upload'),
    path('vehicles/', registered_vehicles_list, name='vehicles_list'),
    path('legislation/', laws, name="legislation"),
    path('search/', search_laws, name='search_laws'),


    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

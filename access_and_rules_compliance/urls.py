from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import allowed_vehicles, laws, search_laws, single_vehicle_upload, bulk_vehicle_entry,\
      registered_vehicles_list, add_vehicle_category, add_vehicle_access_area, get_dropdown_data,\
      bulk_vehicle_save

urlpatterns = [
    #------ general urls-------------------
    # path('choose-tickets', choosetickets_view, name="choose-tickets"),
    path('allowed-vehicles/', allowed_vehicles, name="auto-access"),
    path('vehicles/add/', single_vehicle_upload, name='single_vehicle_upload'),
    path('vehicles/bulk-entry/', bulk_vehicle_entry, name='bulk_vehicle_entry'),
    path('vehicles/', registered_vehicles_list, name='vehicles_list'),
    path('legislation/', laws, name="legislation"),
    path('search/', search_laws, name='search_laws'),
    path('vehicles/add/category/', add_vehicle_category, name='add_vehicle_category'),
    path('vehicles/add/access-area/', add_vehicle_access_area, name='add_vehicle_access_area'),
    path('api/dropdown-data/', get_dropdown_data, name='dropdown_data'),
    path('vehicles/bulk-entry/save/', bulk_vehicle_save, name='bulk_vehicle_save')
    ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

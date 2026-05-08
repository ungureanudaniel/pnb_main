from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    allowed_vehicles, laws, search_laws, single_vehicle_upload, bulk_vehicle_entry,
    registered_vehicles_list, add_vehicle_category, add_vehicle_access_area, get_dropdown_data,
    bulk_vehicle_save, vehicle_detail, edit_vehicle, delete_vehicle,export_filtered_data
)


urlpatterns = [
    # Vehicle access URLs
    path('allowed-vehicles/', allowed_vehicles, name="auto-access"),
    
    # Vehicle management URLs
    path('vehicles/', registered_vehicles_list, name='vehicles_list'),
    path('vehicles/add/', single_vehicle_upload, name='single_vehicle_upload'),
    path('vehicles/bulk-entry/', bulk_vehicle_entry, name='bulk_vehicle_entry'),
    path('vehicles/bulk-entry/save/', bulk_vehicle_save, name='bulk_vehicle_save'),
    
    # Vehicle detail, edit, delete URLs
    path('vehicles/<int:vehicle_id>/', vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:vehicle_id>/edit/', edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:vehicle_id>/delete/', delete_vehicle, name='delete_vehicle'),
    
    # Category and area management
    path('vehicles/category/add/', add_vehicle_category, name='add_vehicle_category'),
    path('vehicles/access-area/add/', add_vehicle_access_area, name='add_vehicle_access_area'),
    
    # Legislation URLs
    path('legislation/', laws, name="legislation"),
    path('legislation/search/', search_laws, name='search_laws'),
    
    # API URLs
    path('api/dropdown-data/', get_dropdown_data, name='dropdown_data'),

    # export xcel
    path('export_filtered_data/', export_filtered_data, name='export_filtered_data')
]

# Static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


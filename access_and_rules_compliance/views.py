from django.shortcuts import render
from services.models import AllowedVehicles
from .models import Law
from django.db.models import Q
from loguru import logger
from .forms import VehicleForm, ExcelUploadForm
from datetime import datetime
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
#=================allowed vehicles version 2===============================
@cache_page(60 * 15)
@login_required(login_url='login')
def allowed_vehicles(request):
    template = 'access/allowed_vehicles.html'
    context = {}

    if request.method == "GET" and request.GET.get('form-type') == "search":
        query = request.GET.get("q", "").replace(" ", "").upper()
        
        if query:
            try:
                # Fetch the most recent permit based on the end date
                vehicles = AllowedVehicles.objects.filter(Q(identification_nr=query)).order_by("end_date").prefetch_related('area')
                print(vehicles)
            except Exception as e:
                messages.error(request, _("An error occurred: {}").format(str(e)))
            try:
                if vehicles:
                    today = datetime.today().date()
                    car_info = []
                    for vehicle in vehicles:
                        start_date = vehicle.start_date
                        end_date = vehicle.end_date
                        if end_date >= today:
                            car_info.append({
                                'owner': vehicle.owner,
                                'identification_nr': vehicle.identification_nr,
                                'area': [a.name for a in vehicle.area.all()],  # Convert related areas to a list of names
                                'permit_nr': vehicle.permit_nr,
                                'start_date': vehicle.start_date,
                                'end_date': vehicle.end_date,
                                'description': vehicle.description,
                            })
                            continue
                    if start_date > today:
                        messages.warning(request, _('Vehicle with plates number {} is not yet allowed in the park! Permit starts on {}.').format(vehicle.identification_nr, start_date))
                    elif start_date <= today and end_date >= today:
                        messages.success(request, _('Vehicle with plates number {} is allowed in the park!').format(vehicle.identification_nr))
                        context.update({"car_info": car_info})
                    else:
                        messages.error(request, _('Vehicle with plates number {} is not authorized!').format(query))
                else:
                    messages.error(request, _('Vehicle with plates number {} is not authorized!').format(query))
            except Exception as e:
                messages.error(request, _("An error occurred: {}").format(str(e)))
        else:
            messages.error(request, _("Invalid search query!"))

    return render(request, template, context)

#=================allowed vehicles input===============================
def single_vehicle_upload(request):
    template = 'access/single_vehicle_upload.html'
    context = {}
    
    if request.method == "POST":
        vehicle_form = VehicleForm(request.POST)
        if vehicle_form.is_valid():
            try:
                vehicle_form.save()
                messages.success(request, _("Vehicle information saved successfully!"))
            except Exception as e:
                messages.error(request, _("An error occurred: {}").format(str(e)))
        else:
            messages.error(request, _("Form is not valid! Please check your input."))
    
    context['vehicle_form'] = VehicleForm()
    return render(request, template, context)

#=================bulk vehicle upload===============================
def bulk_vehicle_upload(request):
    template = 'access/bulk_vehicle_upload.html'
    context = {}
    
    if request.method == "POST":
        excel_form = ExcelUploadForm(request.POST, request.FILES)
        if excel_form.is_valid():
            try:
                # Process the uploaded Excel file
                file = request.FILES['file']
                # Assuming you have a utility function to handle the import
                from access_and_rules_compliance.utils import import_vehicles_from_excel
                result = import_vehicles_from_excel(file)
                messages.success(request, result)
            except Exception as e:
                messages.error(request, _("An error occurred while processing the file: {}").format(str(e)))
        else:
            messages.error(request, _("Invalid form submission! Please check your input."))
    
    context['excel_form'] = ExcelUploadForm()
    return render(request, template, context)

#=================registered vehicles list===============================
def registered_vehicles_list(request):
    template = 'access/registered_vehicles_list.html'
    context = {
        'vehicles': AllowedVehicles.objects.all()
    }
    return render(request, template, context)

#=================allowed vehicles input===============================
# # This view handles the input of allowed vehicles, either through a form or an Excel upload.
# def allowed_vehicles_input(request):
#     template = 'access/add_vehicles.html'
#     context = {}
#     if request.method == "POST":
#         if 'excel_upload' in request.POST:
#             excel_form = ExcelUploadForm(request.POST, request.FILES)
#             if excel_form.is_valid():
#                 try:
#                     # Process the uploaded Excel file
#                     file = request.FILES['file']
#                     # Assuming you have a utility function to handle the import
#                     from access_and_rules_compliance.utils import import_vehicles_from_excel
#                     result = import_vehicles_from_excel(file)
#                     messages.success(request, result)
#                 except Exception as e:
#                     messages.error(request, _("An error occurred while processing the file: {}").format(str(e)))
#             else:
#                 messages.error(request, _("Invalid form submission! Please check your input."))
#         if 'vehicle_form' in request.POST:
#             vehicle_form = VehicleForm(request.POST)
#             if vehicle_form.is_valid():
#                 try:
#                     vehicle_form.save()
#                     messages.success(request, _("Vehicle information saved successfully!"))
#                 except Exception as e:
#                     messages.error(request, _("An error occurred: {}").format(str(e)))
#             else:
#                 messages.error(request, _("Form is not valid! Please check your input."))
#     return render(request, template, context)
#=================laws===============================
def laws(request):
    template = "laws/laws.html"
    context = {"laws":Law.objects.all()}
    return render(request, template, context)
#=================search laws===============================
def search_laws(request):
    template = "laws/search_laws.html"
    title = request.GET.get('title', '')
    doc_nr = request.GET.get('doc_nr', '')
    publish_year = request.GET.get('publish_year', '')
    doc_type = request.GET.get('doc_type', '')

    # Start with the full queryset
    query= Q()

    # Apply filters based on the presence of query parameters
    if title:
        query &= Q(title__icontains=title)
    if doc_nr:
        query &= Q(doc_nr__icontains=doc_nr)
    if publish_year:
        try:
            # Try to parse the date string
            year = int(publish_year)
            query &= Q(publish_date__year=year)
        except ValueError:
            # Handle invalid date format
            query = Q()
    if doc_type:
        query = Q(doc_nr__icontains=doc_nr)

    return render(request, template, {'laws': Law.objects.filter(query)})
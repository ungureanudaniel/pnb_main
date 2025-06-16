from django.shortcuts import render, redirect
from services.models import AllowedVehicles, VehicleCategory, AccessArea
from .models import Law
from django.db.models import Q
from loguru import logger
from django.http import JsonResponse
import json
from .forms import VehicleAccessAreaForm, VehicleForm, ExcelUploadForm, VehicleCategoryForm
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

#=================add vehicle category===============================
@login_required(login_url='signin')
def add_vehicle_category(request):
    """
    This view handles the addition of vehicle categories.
    It is currently a placeholder and does not implement any functionality.
    """
    template = 'access/add_vehicle_category.html'
    context = {}
    
    if request.method == "POST":
        form = VehicleCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Vehicle category added successfully!"))
            return redirect('single_vehicle_upload')
        else:
            print(form.errors)
            messages.error(request, _("Form is not valid! Please check your input.{}".format(form.errors)))
    else:
        form = VehicleCategoryForm()
    context['form'] = form
    return render(request, template, context)

@login_required(login_url='signin')
def add_vehicle_access_area(request):
    """
    This view handles the vehicle access area.
    It is currently a placeholder and does not implement any functionality.
    """
    template = 'access/add_vehicle_access_area.html'
    context = {}
    
    if request.method == "POST":
        form = VehicleAccessAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Vehicle access area added successfully!"))
            return redirect('single_vehicle_upload')
        else:
            print(form.errors)
            messages.error(request, _("Form is not valid! Please check your input.{}".format(form.errors)))
    else:
        form = VehicleAccessAreaForm()
    context['form'] = form
    return render(request, template, context)

#=================allowed vehicles version 2===============================
@cache_page(60 * 15)
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
@login_required(login_url='signin')
def single_vehicle_upload(request):
    template = 'access/single_vehicle_upload.html'
    context = {}
    
    if request.method == "POST":
        vehicle_form = VehicleForm(request.POST)
        if vehicle_form.is_valid():
            try:
                vehicle_form.owner = vehicle_form.cleaned_data['owner'].capitalize()
                vehicle_form.save()
                messages.success(request, _("Vehicle information saved successfully!"))
            except Exception as e:
                messages.error(request, _("An error occurred: {}").format(str(e)))
        else:
            messages.error(request, _("Form is not valid! Please check your input. ({}").format(vehicle_form.errors))
    else:
        vehicle_form = VehicleForm()
    context['vehicle_form'] = vehicle_form
    return render(request, template, context)

#================= api for serving dropdown list data ===============================
def get_dropdown_data(request):
    categories = list(VehicleCategory.objects.values_list('title', flat=True))
    areas = list(AccessArea.objects.values_list('name', flat=True))
    return JsonResponse({
        'categories': categories,
        'areas': areas
    })

#=================bulk vehicle upload===============================
@login_required(login_url='signin')
def bulk_vehicle_entry(request):
    template = 'access/bulk_vehicle_entry.html'
    """Render the editable table page for bulk vehicle entry."""
    categories = list(VehicleCategory.objects.values_list('title', flat=True))
    areas = list(AccessArea.objects.values_list('name', flat=True))

    return render(request, template, {
        'categories': categories,
        'areas': areas,
    })

#=================bulk vehicle save======================================
@login_required(login_url='signin')
def bulk_vehicle_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            created = 0
            for row in data:
                if any(row):  # Skip empty rows
                    AllowedVehicles.objects.create(
                        owner=row[0],
                        categ=row[1],
                        identification_nr=row[2],
                        zona=row[3],
                        nr_aviz=row[4],
                        data_inceput=row[5],
                        data_sfarsit=row[6],
                        descriere=row[7],
                    )
                    created += 1
            return JsonResponse({'message': f"{created} vehicles saved successfully."})
        except Exception as e:
            return JsonResponse({'message': f"Error: {str(e)}"}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=405)

#=================registered vehicles list===============================
@login_required(login_url='signin')
def registered_vehicles_list(request):
    template = 'access/registered_vehicles_list.html'

    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    area_id = request.GET.get('area', '').strip()

    vehicles = AllowedVehicles.objects.all().order_by('-timestamp').prefetch_related('area')
    
    if query:
        vehicles = vehicles.filter(
            Q(identification_nr__icontains=query) |
            Q(owner__icontains=query)
        )
    
    if category_id:
        vehicles = vehicles.filter(categ_id=category_id)
    
    if area_id:
        vehicles = vehicles.filter(area__id=area_id)

    paginator = Paginator(vehicles, 5)  # Show 20 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'vehicles': page_obj,
        'categories': VehicleCategory.objects.all(),
        'areas': AccessArea.objects.all(),
        'query': query,
        'selected_category': category_id,
        'selected_area': area_id,
    }
    return render(request, template, context)

#=================allowed vehicles input===============================

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
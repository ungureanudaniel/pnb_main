from django.shortcuts import render, redirect
from services.models import AllowedVehicles, VehicleCategory, AccessArea
from .models import Law
from django.db.models import Q
from django.http import JsonResponse
import json
import traceback
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
                vehicles = AllowedVehicles.objects.filter(
                    identification_nr=query
                ).order_by("-end_date").prefetch_related('area')  # Use -end_date to get latest first
                
                if vehicles.exists():
                    today = datetime.today().date()
                    car_info = []
                    valid_vehicle_found = False
                    
                    for vehicle in vehicles:
                        start_date = vehicle.start_date
                        end_date = vehicle.end_date
                        
                        if start_date <= today <= end_date:
                            car_info.append({
                                'owner': vehicle.owner,
                                'identification_nr': vehicle.identification_nr,
                                'area': [a.name for a in vehicle.area.all()],
                                'permit_nr': vehicle.permit_nr,
                                'start_date': vehicle.start_date,
                                'end_date': vehicle.end_date,
                                'description': vehicle.description,
                            })
                            valid_vehicle_found = True
                            
                            messages.success(
                                request, 
                                _('Vehicle with plates number {} is allowed in the park!').format(vehicle.identification_nr)
                            )
                        elif start_date > today:
                            messages.warning(
                                request, 
                                _('Vehicle with plates number {} is not yet allowed! Permit starts on {}.').format(
                                    vehicle.identification_nr, 
                                    start_date.strftime('%d-%m-%Y')
                                )
                            )
                        else:
                            messages.error(
                                request, 
                                _('Vehicle with plates number {} permit expired on {}.').format(
                                    vehicle.identification_nr,
                                    end_date.strftime('%d-%m-%Y')
                                )
                            )
                    
                    if valid_vehicle_found:
                        context.update({"car_info": car_info})
                    else:
                        messages.error(request, _('No active permit found for vehicle {}.').format(query))
                else:
                    messages.error(request, _('Vehicle with plates number {} is not registered!').format(query))
            except Exception as e:
                messages.error(request, _("An error occurred: {}").format(str(e)))
        else:
            messages.error(request, _("Please enter a valid license plate number."))

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

@login_required(login_url='signin')
def vehicle_detail(request, vehicle_id):
    template = 'access/vehicle_detail.html'
    
    try:
        vehicle = AllowedVehicles.objects.get(id=vehicle_id)
        context = {
            'vehicle': vehicle,
            'is_active': vehicle.start_date <= datetime.today().date() <= vehicle.end_date if vehicle.end_date else False,
            'days_remaining': (vehicle.end_date - datetime.today().date()).days if vehicle.end_date and vehicle.end_date >= datetime.today().date() else 0,
        }
        return render(request, template, context)
    except AllowedVehicles.DoesNotExist:
        messages.error(request, _("Vehicle not found."))
        return redirect('registered_vehicles_list')

@login_required(login_url='signin')
def edit_vehicle(request, vehicle_id):
    template = 'access/edit_vehicle.html'
    
    try:
        vehicle = AllowedVehicles.objects.get(id=vehicle_id)
    except AllowedVehicles.DoesNotExist:
        messages.error(request, _("Vehicle not found."))
        return redirect('registered_vehicles_list')
    
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, _("Vehicle information updated successfully!"))
            return redirect('vehicle_detail', vehicle_id=vehicle.id)
        else:
            messages.error(request, _("Form is not valid! Please check your input. {}".format(form.errors)))
    else:
        form = VehicleForm(instance=vehicle)
    
    context = {
        'form': form,
        'vehicle': vehicle,
    }
    return render(request, template, context)

@login_required(login_url='signin')
def delete_vehicle(request, vehicle_id):
    if request.method == "POST":
        try:
            vehicle = AllowedVehicles.objects.get(id=vehicle_id)
            identification_nr = vehicle.identification_nr
            vehicle.delete()
            messages.success(request, _("Vehicle {} deleted successfully!").format(identification_nr))
        except AllowedVehicles.DoesNotExist:
            messages.error(request, _("Vehicle not found."))
        
        return redirect('registered_vehicles_list')
    
    return redirect('registered_vehicles_list')

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
            errors = []
            
            for idx, row in enumerate(data):
                if not row or not any(row):
                    continue
                
                try:
                    # Validate required fields
                    if len(row) < 7:
                        errors.append(f"Row {idx + 1}: Missing required fields")
                        continue
                    
                    owner = str(row[0]).strip() if row[0] else ""
                    categ = str(row[1]).strip() if row[1] else ""
                    identification_nr = str(row[2]).strip().upper().replace(" ", "") if row[2] else ""
                    zona = str(row[3]).strip() if row[3] else ""
                    nr_aviz = str(row[4]).strip() if row[4] else ""
                    
                    if not all([owner, categ, identification_nr, zona, nr_aviz]):
                        errors.append(f"Row {idx + 1}: Missing required fields (owner, category, license plate, area, permit number)")
                        continue
                    
                    # Get or create category
                    categ_obj, _ = VehicleCategory.objects.get_or_create(title=categ)
                    
                    # Get or create area
                    zona_obj, _ = AccessArea.objects.get_or_create(name=zona)
                    
                    # Parse dates
                    data_inceput = None
                    data_sfarsit = None
                    
                    if row[5]:
                        try:
                            data_inceput = datetime.strptime(str(row[5]), '%d-%m-%Y').date()
                        except ValueError:
                            errors.append(f"Row {idx + 1}: Invalid start date format. Use DD-MM-YYYY")
                            continue
                    
                    if row[6]:
                        try:
                            data_sfarsit = datetime.strptime(str(row[6]), '%d-%m-%Y').date()
                        except ValueError:
                            errors.append(f"Row {idx + 1}: Invalid end date format. Use DD-MM-YYYY")
                            continue
                    
                    descriere = str(row[7]).strip() if len(row) > 7 and row[7] else ""
                    
                    # Check for duplicate
                    existing = AllowedVehicles.objects.filter(identification_nr=identification_nr).first()
                    if existing:
                        errors.append(f"Row {idx + 1}: Vehicle {identification_nr} already exists (Permit: {existing.permit_nr})")
                        continue
                    
                    # Create vehicle
                    vehicle = AllowedVehicles.objects.create(
                        owner=owner,
                        categ=categ_obj,
                        identification_nr=identification_nr,
                        permit_nr=nr_aviz,
                        start_date=data_inceput,
                        end_date=data_sfarsit,
                        description=descriere,
                    )
                    vehicle.area.set([zona_obj])
                    created += 1
                    
                except Exception as inner_e:
                    errors.append(f"Row {idx + 1}: {str(inner_e)}")
                    traceback.print_exc()
            
            if errors:
                return JsonResponse({
                    'message': f"{created} vehicles saved with {len(errors)} errors.",
                    'errors': errors
                }, status=207)  # Multi-Status
            else:
                return JsonResponse({'message': f"{created} vehicles saved successfully."})
                
        except Exception as e:
            print("Data received:", request.body.decode())
            traceback.print_exc()
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
    laws_list = Law.objects.all().order_by('-publish_date')
    
    paginator = Paginator(laws_list, 10)  # Show 10 laws per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "laws": page_obj,
        "page_obj": page_obj,
    }
    return render(request, template, context)
#=================search laws===============================
def search_laws(request):
    template = "laws/search_laws.html"
    title = request.GET.get('title', '')
    doc_nr = request.GET.get('doc_nr', '')
    publish_year = request.GET.get('publish_year', '')
    doc_type = request.GET.get('doc_type', '')

    # Build query
    query = Q()
    
    if title:
        query &= Q(title__icontains=title)
    if doc_nr:
        query &= Q(doc_nr__icontains=doc_nr)
    if publish_year:
        try:
            year = int(publish_year)
            query &= Q(publish_date__year=year)
        except ValueError:
            pass
    if doc_type:
        query &= Q(doc_type__icontains=doc_type)  # Fixed this line
    
    laws = Law.objects.filter(query) if query else Law.objects.none()
    
    context = {
        'laws': laws,
        'search_params': {
            'title': title,
            'doc_nr': doc_nr,
            'publish_year': publish_year,
            'doc_type': doc_type,
        }
    }
    return render(request, template, context)
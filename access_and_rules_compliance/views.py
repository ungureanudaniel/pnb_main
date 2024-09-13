from django.shortcuts import render
from services.models import AllowedVehicles
from .models import Law
from loguru import logger
from datetime import datetime
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

#=================allowed vehicles version 2===============================
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
#=================laws===============================
def laws(request):
    template = "laws/laws.html"
    context = {"laws":Law.objects.all()}
    return render(request, template, context)


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from parking.forms import VehicleCategoryForm, VehicleRegistrationForm
from .models import VehicleCategory, VehicleRegistration


def vehicle_category(request):
    form = VehicleCategoryForm()

    if request.method == 'POST':
        form = VehicleCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('vehicle_category_list')

    return render(request, 'add_category.html', {'form': form})


def vehicle_category_list(request):
    categories = VehicleCategory.objects.all()
    return render(request, "vehicle_category.html", {"categories": categories})

def register_vehicle(request):
    form = VehicleRegistrationForm()

    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.arrival_time = timezone.now()
            vehicle.status = "parked"
            vehicle.save()

            return redirect('vehicle_registration_list')

    return render(request, 'vehicle_registration.html', {'form': form})


def vehicle_registration_list(request):
    vehicles = VehicleRegistration.objects.all().order_by("-arrival_time")
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def dashboard(request):

    vehicles = VehicleRegistration.objects.all().order_by("-arrival_time")

    parked = vehicles.filter(status="parked").count()
    exited = vehicles.filter(status="signed_out").count()

    revenue = sum(v.fee for v in vehicles.filter(status="signed_out"))

    return render(request, "dashboard.html", {
        "vehicles": vehicles,
        "parked": parked,
        "exited": exited,
        "total_revenue": revenue,
    })

def checkout_vehicle(request, pk):

    vehicle = get_object_or_404(VehicleRegistration, id=pk)

    if request.method == "POST":

        vehicle.departure_time = timezone.now()
#
        duration = vehicle.departure_time - vehicle.arrival_time
        hours = duration.total_seconds() / 3600


        category = vehicle.vehicle_type

        is_day = 6 <= vehicle.arrival_time.hour < 19

        if hours < 3:
            fee = category.short_stay_rate
        else:
            fee = category.day_rate if is_day else category.night_rate

        vehicle.fee = fee
        vehicle.status = "signed_out"
        vehicle.save()

        return redirect('print_receipt', pk=vehicle.id)

    return render(request, "exit.html", {"vehicle": vehicle})

# =========================
# RECEIPT PAGE (NEW OPTIONAL)
# =========================
def print_receipt(request, pk):

    vehicle = get_object_or_404(VehicleRegistration, id=pk)

    if vehicle.departure_time and vehicle.arrival_time:
        duration = vehicle.departure_time - vehicle.arrival_time
        hours = duration.total_seconds() / 3600
    else:
        hours = 0

    return render(request, "receipt.html", {
        "vehicle": vehicle,
        "hours": round(hours, 2),
        "fee": vehicle.fee
    })
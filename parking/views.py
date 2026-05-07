from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from parking.forms import VehicleCategoryForm, VehicleRegistrationForm, CheckoutForm
from .models import VehicleCategory, VehicleRegistration


# ✅ PROFESSIONAL ACCESS HANDLER
def no_access(request):
    messages.error(request, "You are not authorized to access this page.")
    return redirect("dashboard")


# =========================
# CATEGORY
# =========================

@login_required
def vehicle_category(request):
    if request.user.role != "ADMIN":
        return no_access(request)

    form = VehicleCategoryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('vehicle_category_list')

    return render(request, 'add_category.html', {'form': form})


@login_required
def vehicle_category_list(request):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request)

    categories = VehicleCategory.objects.all()
    return render(request, "vehicle_category.html", {"categories": categories})


# =========================
# VEHICLE REGISTRATION
# =========================

@login_required
def register_vehicle(request):
    if request.user.role != "ATTENDANT":
        return no_access(request)

    form = VehicleRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.arrival_time = timezone.now()
            vehicle.status = "parked"
            vehicle.registered_by = request.user
            vehicle.save()

            messages.success(request, "Vehicle registered successfully.")
            return redirect('dashboard')

    return render(request, 'vehicle_registration.html', {'form': form})


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request)

    all_vehicles = VehicleRegistration.objects.all().order_by("-arrival_time")

    parked_vehicles = all_vehicles.filter(status="parked")
    signed_out_vehicles = all_vehicles.filter(status="signed_out")

    cards = [
        {
            "title": "Total Vehicles",
            "value": all_vehicles.count(),
            "icon": "bi-car-front",
            "text_color": "text-primary",
        },
        {
            "title": "Currently Parked",
            "value": parked_vehicles.count(),
            "icon": "bi-check-circle",
            "text_color": "text-success",
        },
        {
            "title": "Checked Out",
            "value": signed_out_vehicles.count(),
            "icon": "bi-box-arrow-right",
            "text_color": "text-dark",
        },
    ]

    context = {
        "cards": cards,
        "parked_vehicles": parked_vehicles,
        "signed_out_vehicles": signed_out_vehicles,
    }

    return render(request, "dashboard.html", context)


# =========================
# CHECKOUT (UPDATED ✅)
# =========================

@login_required
def checkout_vehicle(request, pk):
    if request.user.role != "ATTENDANT":
        return no_access(request)

    vehicle = get_object_or_404(VehicleRegistration, id=pk)

    if request.method == "POST":
        form = CheckoutForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.departure_time = timezone.now()

            # ✅ USE MODEL METHOD (IMPORTANT FIX)
            fee, rate_type = vehicle.calculate_fee()

            vehicle.fee = fee
            vehicle.rate_type = rate_type
            vehicle.status = "signed_out"

            vehicle.save()

            messages.success(request, "Vehicle checked out successfully.")
            return redirect("dashboard")
    else:
        form = CheckoutForm(instance=vehicle)

    # preview before submit
    fee, rate_type = vehicle.calculate_fee()
    duration = (timezone.now() - vehicle.arrival_time).total_seconds() / 3600

    return render(request, "exit.html", {
        "vehicle": vehicle,
        "form": form,
        "duration": round(duration, 2),
        "fee": fee,
        "rate_type": rate_type
    })


# =========================
# RECEIPT
# =========================

@login_required
def print_receipt(request, pk):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request)

    vehicle = get_object_or_404(VehicleRegistration, id=pk)

    if vehicle.departure_time and vehicle.arrival_time:
        duration = (vehicle.departure_time - vehicle.arrival_time).total_seconds() / 3600
    else:
        duration = 0

    context = {
        "vehicle": vehicle,
        "hours": round(duration, 2),
        "fee": vehicle.fee,
        "rate_type": vehicle.rate_type or "pending"
    }

    return render(request, "receipt.html", context)


# =========================
# EDIT VEHICLE
# =========================

@login_required
def edit_vehicle(request, id):
    vehicle = get_object_or_404(VehicleRegistration, id=id)

    if vehicle.status != "parked":
        messages.error(request, "You cannot edit a signed-out vehicle.")
        return redirect('dashboard')

    form = VehicleRegistrationForm(request.POST or None, instance=vehicle)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect('dashboard')

    return render(request, 'edit_vehicle.html', {'form': form})
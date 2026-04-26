from django.shortcuts import render,redirect,get_object_or_404
from parking.models import VehicleRegistration
from services.models import TyreService, BatteryService
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def no_access():
    return HttpResponseForbidden("You do not have permission to access this page.")


def report_dashboard(request):
    if request.user.role != 'ADMIN':
        return no_access()

    date = request.GET.get("date")

    # SIGNED OUT VEHICLES
    vehicles = VehicleRegistration.objects.filter(status="signed_out").order_by("-departure_time")

    if date:
        vehicles = vehicles.filter(departure_time__date=date)

    # PARKING REVENUE
    parking_total = sum(v.fee for v in vehicles)

    # TYRE REVENUE
    tyre_services = TyreService.objects.all()
    if date:
        tyre_services = tyre_services.filter(date__date=date)

    tyre_total = sum(t.service.price for t in tyre_services)

    # BATTERY REVENUE
    battery_services = BatteryService.objects.all()
    if date:
        battery_services = battery_services.filter(date__date=date)

    battery_total = sum(b.price for b in battery_services)

    # DAILY TOTAL
    total_revenue = parking_total + tyre_total + battery_total

    # OVERALL TOTAL (ALL TIME)
    all_vehicles = VehicleRegistration.objects.filter(status="signed_out")
    overall_parking = sum(v.fee for v in all_vehicles)
    overall_tyre = sum(t.service.price for t in TyreService.objects.all())
    overall_battery = sum(b.price for b in BatteryService.objects.all())

    overall_total = overall_parking + overall_tyre + overall_battery

    # ✅ NOW create cards (after values exist)
    cards = [
        {
            "title": "Parking Revenue",
            "value": f"UGX {parking_total}",
            "icon": "bi-car-front",
            "text_color": "text-primary",
        },
        {
            "title": "Tyre Revenue",
            "value": f"UGX {tyre_total}",
            "icon": "bi-wrench",
            "text_color": "text-success",
        },
        {
            "title": "Battery Revenue",
            "value": f"UGX {battery_total}",
            "icon": "bi-battery-half",
            "text_color": "text-dark",
        },
    ]

    # CONTEXT
    context = {
        "cards": cards,
        "vehicles": vehicles,
        "parking_total": parking_total,
        "tyre_total": tyre_total,
        "battery_total": battery_total,
        "total_revenue": total_revenue,
        "overall_total": overall_total,
        "date": date
    }

    return render(request, "report.html", context)

@login_required
def delete_vehicle(request, id):
    vehicle = get_object_or_404(VehicleRegistration, id=id)

    # 🔒 Only admin allowed
    if request.user.role != "ADMIN":
        messages.error(request, "You are not allowed to delete records.")
        return redirect('admin_dashboard')

    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('report_dashboard')

    return render(request, 'delete_record.html', {'vehicle': vehicle})
from django.shortcuts import render
from parking.models import VehicleRegistration
from services.models import TyreService, BatteryService

def report_dashboard(request):

    date = request.GET.get("date")

    vehicles = VehicleRegistration.objects.filter(status="signed_out").order_by("-departure_time")

    if date:
        vehicles = vehicles.filter(departure_time__date=date)

    parking_total = 0
    for v in vehicles:
        parking_total += v.fee

    tyre_total = 0
    tyre_services = TyreService.objects.all()
    if date:
        tyre_services = tyre_services.filter(date__date=date)

    for t in tyre_services:
        tyre_total += t.service.price

    battery_total = 0
    battery_services = BatteryService.objects.all()
    if date:
        battery_services = battery_services.filter(date__date=date)

    for b in battery_services:
        battery_total += b.price

    total_revenue = parking_total + tyre_total + battery_total
    

    return render(request, "report.html", {
        "vehicles": vehicles,
        "parking_total": parking_total,
        "tyre_total": tyre_total,
        "battery_total": battery_total,
        "total_revenue": total_revenue,
        "date": date
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import ServicePrice, TyreService, BatteryService
from .forms import ServicePriceForm, TyreServiceForm, BatteryServiceForm


# create logic here
def add_service_price(request):
    form = ServicePriceForm()

    if request.method == "POST":
        form = ServicePriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_price_list")

    return render(request, "add_price.html", {"form": form})


def service_price_list(request):
    prices = ServicePrice.objects.all()
    return render(request, "price_list.html", {"prices": prices})


def add_tyre_service(request):
    form = TyreServiceForm()

    if request.method == "POST":
        form = TyreServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tyre_list")

    return render(request, "add_tyre.html", {"form": form})


def tyre_list(request):
    services = TyreService.objects.all().order_by("-date")
    return render(request, "tyre_list.html", {"services": services})


def tyre_receipt(request, pk):
    service = get_object_or_404(TyreService, id=pk)
    price = service.service.price

    return render(request, "tyre_receipt.html", {
        "service": service,
        "price": price
    })


def add_battery_service(request):
    form = BatteryServiceForm()

    if request.method == "POST":
        form = BatteryServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("battery_list")

    return render(request, "add_battery.html", {"form": form})


def battery_list(request):
    batteries = BatteryService.objects.all().order_by("-date")
    return render(request, "battery_list.html", {"batteries": batteries})


def battery_receipt(request, pk):
    service = get_object_or_404(BatteryService, id=pk)

    return render(request, "battery_receipt.html", {
        "service": service,
        "price": service.price
    })


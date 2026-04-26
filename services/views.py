from django.shortcuts import render, redirect, get_object_or_404
from .models import ServicePrice, TyreService, BatteryService
from .forms import ServicePriceForm, TyreServiceForm, BatteryServiceForm
from django.contrib import messages


# =========================
# SERVICE PRICE
# =========================
def add_service_price(request):

    # 🔒 ROLE CHECK (SIMPLE STYLE)
    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    form = ServicePriceForm()

    if request.method == "POST":
        form = ServicePriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_price_list")

    return render(request, "add_price.html", {"form": form})


def service_price_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    prices = ServicePrice.objects.all()
    return render(request, "price_list.html", {"prices": prices})


def edit_price(request, id):
    price = get_object_or_404(ServicePrice, id=id)

    if request.method == "POST":
        form = ServicePriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            messages.success(request, "Price updated successfully.")
            return redirect('service_price_list')
    else:
        form = ServicePriceForm(instance=price)

    return render(request, 'edit_price.html', {'form': form})

def delete_price(request, id):
    price = get_object_or_404(ServicePrice, id=id)

    if request.method == "POST":
        price.delete()
        messages.success(request, "Price deleted successfully.")
        return redirect('service_price_list')

    return render(request, 'delete_price.html', {'price': price})


# =========================
# TYRE SERVICE
# =========================
def add_tyre_service(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    form = TyreServiceForm()

    if request.method == "POST":
        form = TyreServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tyre_list')

    return render(request, "add_tyre.html", {"form": form})


def tyre_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    services = TyreService.objects.all().order_by("-date")
    return render(request, "tyre_list.html", {"services": services})

def tyre_detail(request, id):
    tyre = get_object_or_404(TyreService, id=id)
    return render(request, 'tyre_detail.html', {'tyre': tyre})

def edit_tyre(request, id):
    tyre = get_object_or_404(TyreService, id=id)

    if request.method == "POST":
        form = TyreServiceForm(request.POST, instance=tyre)
        if form.is_valid():
            form.save()
            messages.success(request, "Tyre service updated successfully.")
            return redirect('tyre_detail', id=tyre.id)
    else:
        form = TyreServiceForm(instance=tyre)

    return render(request, 'edit_tyre.html', {'form': form})


def delete_tyre(request, id):
    tyre = get_object_or_404(TyreService, id=id)

    if request.method == "POST":
        tyre.delete()
        messages.success(request, "Tyre service deleted.")
        return redirect('tyre_list')

    return render(request, 'delete_tyre.html', {'tyre': tyre})




def tyre_receipt(request, pk):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    service = get_object_or_404(TyreService, id=pk)
    price = service.service.price

    return render(request, "tyre_receipt.html", {
        "service": service,
        "price": price
    })


# =========================
# BATTERY SERVICE
# =========================
def add_battery_service(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    form = BatteryServiceForm()

    if request.method == "POST":
        form = BatteryServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("battery_list")

    return render(request, "add_battery.html", {"form": form})


def battery_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    batteries = BatteryService.objects.all().order_by("-date")
    return render(request, "battery_list.html", {"batteries": batteries})


def battery_receipt(request, pk):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    service = get_object_or_404(BatteryService, id=pk)

    return render(request, "battery_receipt.html", {
        "service": service,
        "price": service.price
    })


def battery_detail(request, id):
    battery = get_object_or_404(BatteryService, id=id)
    return render(request, 'battery_detail.html', {'battery': battery})


def edit_battery(request, id):
    battery = get_object_or_404(BatteryService, id=id)

    if request.method == "POST":
        form = BatteryServiceForm(request.POST, instance=battery)
        if form.is_valid():
            form.save()
            messages.success(request, "Battery service updated successfully.")
            return redirect('battery_list')  
    else:
        form = BatteryServiceForm(instance=battery)

    return render(request, 'edit_battery.html', {'form': form})


def delete_battery(request, id):
    battery = get_object_or_404(BatteryService, id=id)

    if request.method == "POST":
        battery.delete()
        messages.success(request, "Battery service deleted successfully.")
        return redirect('battery_list')

    return render(request, 'delete_battery.html', {'battery': battery})
from django import forms
from .models import ServicePrice, TyreService, BatteryService


# =========================
# SERVICE PRICE FORM
# =========================
class ServicePriceForm(forms.ModelForm):
    class Meta:
        model = ServicePrice
        fields = "__all__"


# =========================
# TYRE SERVICE FORM
# =========================
class TyreServiceForm(forms.ModelForm):
    class Meta:
        model = TyreService
        fields = [
            "vehicle_plate",
            "service",
            "registered_by"
        ]


# =========================
# BATTERY SERVICE FORM
# =========================
class BatteryServiceForm(forms.ModelForm):
    class Meta:
        model = BatteryService
        fields = [
            "customer_name",
            "battery_type",
            "price",
            "registered_by"
        ]
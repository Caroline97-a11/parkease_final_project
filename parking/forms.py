from django import forms
from parking.models import VehicleCategory,VehicleRegistration

class VehicleCategoryForm(forms.ModelForm):
    class Meta:
        model = VehicleCategory
        fields = '__all__'


class VehicleRegistrationForm(forms.ModelForm):

    class Meta:
        model = VehicleRegistration

        fields = [
            "vehicle_type",
            "plate_number",
            "model",
            "color",
            "driver_name",
            "driver_status",
            "phone_number",
            "nin_number",
        ]
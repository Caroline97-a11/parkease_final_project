from django import forms
from parking.models import VehicleCategory, VehicleRegistration


class VehicleCategoryForm(forms.ModelForm):
    class Meta:
        model = VehicleCategory
        fields = "__all__"


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
        widgets = {
            "vehicle_type": forms.Select(attrs={"class": "form-select"}),
            "plate_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "UA432AT"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "driver_status": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+2567XXXXXXXX"}),
            "nin_number": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_driver_name(self):
        name = self.cleaned_data.get("driver_name")
        if len(name) < 3:
            raise forms.ValidationError("Driver name must be at least 3 characters.")
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Driver name must contain letters only.")
        return name.title()

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.startswith("+256"):
            raise forms.ValidationError("Phone number must start with +256.")
        if not phone[1:].isdigit():
            raise forms.ValidationError("Phone number must contain digits only.")
        if len(phone) != 13:
            raise forms.ValidationError("Phone number must be in format +256XXXXXXXXX.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get("vehicle_type")
        nin_number = cleaned_data.get("nin_number")

        if vehicle_type and vehicle_type.vehicle_type == "Boda-boda":
            if not nin_number:
                self.add_error("nin_number", "NIN is required for Boda-boda drivers.")

        if nin_number:
            if not nin_number.isalnum():
                self.add_error("nin_number", "NIN must contain letters and numbers only.")

            if not nin_number.startswith("C"):
                self.add_error("nin_number", "NIN must start with letter C.")

            if len(nin_number) != 14:
                self.add_error("nin_number", "NIN must be exactly 14 characters.")

        return cleaned_data


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = ["driver_name", "phone_number", "nin_number", "driver_status"]
        widgets = {
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "nin_number": forms.TextInput(attrs={"class": "form-control"}),
            "driver_status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_driver_name(self):
        name = self.cleaned_data.get("driver_name")
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain letters only.")
        return name.title()

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.startswith("+256"):
            raise forms.ValidationError("Phone must start with +256.")
        if not phone[1:].isdigit():
            raise forms.ValidationError("Phone must contain digits only.")
        return phone
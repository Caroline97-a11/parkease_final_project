from django.db import models
import uuid
from django.utils import timezone
from staff.models import Staff

# # Create your models here.

class VehicleCategory(models.Model):

    VEHICLE_TYPES = [
        ("truck", "Truck"),
        ("car", "Personal Car"),
        ("taxi", "Taxi"),
        ("coaster", "Coaster"),
        ("boda", "Boda-boda"),
    ]

    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES, unique=True)
    day_rate = models.IntegerField()
    night_rate = models.IntegerField()
    short_stay_rate = models.IntegerField()

    def __str__(self):
        return self.vehicle_type


class VehicleRegistration(models.Model):

    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    STATUS_CHOICES = [('parked', 'Parked'), ('signed_out', 'Signed Out')]

    vehicle_type = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)

    plate_number = models.CharField(max_length=10)
    model = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100)

    driver_name = models.CharField(max_length=100)
    driver_status = models.CharField(max_length=10, choices=GENDER_CHOICES)

    phone_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True)

    arrival_time = models.DateTimeField(default=timezone.now)
    departure_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="parked")

    ticket_number = models.CharField(max_length=20, unique=True, editable=False)

    fee = models.IntegerField(default=0)
    registered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate_number} ({self.ticket_number})"
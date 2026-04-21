from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class VehicleCategory(models.Model):
    
    VEHICLE_TYPES = [
        ("truck", "Truck"),
        ("car", "Personal Car"),
        ("taxi", "Taxi"),
        ("coaster", "Coaster"),
        ("boda", "Boda-boda"),
    ]

    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    day_rate = models.IntegerField()        
    night_rate = models.IntegerField()      
    short_stay_rate = models.IntegerField() 

    class Meta:
        verbose_name_plural = "Vehicle Categories"

    def __str__(self):
        return self.name


class VehicleRegistration(models.Model):

    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    VEHICLE_STATUS =[('parked','Parked'), ('Signed_out','signed_out')]

    vehicle_type = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=10)
    model_color = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    driver_status = models.CharField(max_length=100, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True)
    arrival_time = models.DateTimeField(default=timezone.now)
    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate_number} ({self.ticket_number})"
    
    
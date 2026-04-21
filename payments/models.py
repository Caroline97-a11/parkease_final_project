from django.db import models
from parking.models import VehicleRegistration 
from django.utils import timezone
import uuid

# Create your models here.

class Payment(models.Model):
    
    # OneToOneField relationship ensures one vehicle has exactly one payment
    vehicle = models.OneToOneField(VehicleRegistration, on_delete=models.CASCADE, related_name='payment_info')
    receiver_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    exit_time = models.DateTimeField(default=timezone.now)
    amount_paid = models.IntegerField()
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"REC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.vehicle.plate_number}"
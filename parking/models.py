from django.db import models
import uuid
from django.utils import timezone
from staff.models import Staff


class VehicleCategory(models.Model):

    VEHICLE_TYPES = [
        ("Truck", "Truck"),
        ("Personal car", "Personal car"),
        ("Taxi", "Taxi"),
        ("Coaster", "Coaster"),
        ("Boda-boda", "Boda-boda"),
    ]

    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES, unique=True)

    day_rate = models.IntegerField()
    night_rate = models.IntegerField()
    short_stay_rate = models.IntegerField()

    def __str__(self):
        return self.vehicle_type


class VehicleRegistration(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    STATUS_CHOICES = [
        ('parked', 'Parked'),
        ('signed_out', 'Signed Out')
    ]

    RATE_TYPE_CHOICES = [
    ("day", "Day"),
    ("night", "Night"),
    ("short", "Short Stay"),
    ("overstay", "Overstay"),  # ✅ ADD THIS
]

    vehicle_type = models.ForeignKey(
        VehicleCategory,
        on_delete=models.CASCADE
    )

    plate_number = models.CharField(max_length=10)
    model = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100)

    driver_name = models.CharField(max_length=100)
    driver_status = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    phone_number = models.CharField(max_length=15)
    nin_number = models.CharField(max_length=20, blank=True, null=True)

    arrival_time = models.DateTimeField(default=timezone.now)
    departure_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="parked"
    )

    ticket_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    fee = models.IntegerField(default=0)

    rate_type = models.CharField(
        max_length=10,
        choices=RATE_TYPE_CHOICES,
        null=True,
        blank=True
    )

    registered_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True
    )

    # ✅ AUTO GENERATE TICKET
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

def calculate_fee(self):
    if not self.arrival_time:
        return 0, None

    end_time = self.departure_time or timezone.now()
    total_hours = (end_time - self.arrival_time).total_seconds() / 3600

    category = self.vehicle_type

    # ✅ SHORT STAY
    if total_hours <= 3:
        return category.short_stay_rate, "short"

    fee = 0

    # ✅ FULL DAYS
    full_days = int(total_hours // 24)
    remaining_hours = total_hours % 24

    fee += full_days * category.day_rate

    # ✅ DETERMINE RATE TYPE FIRST
    if total_hours > 24:
        rate_type = "overstay"   # ✅ MAIN FIX
    else:
        current_hour = timezone.localtime(end_time).hour

        if 6 <= current_hour < 19:
            rate_type = "day"
        else:
            rate_type = "night"

    # ✅ ADD REMAINING HOURS COST
    if remaining_hours > 0:
        current_hour = timezone.localtime(end_time).hour

        if 6 <= current_hour < 19:
            fee += category.day_rate
        else:
            fee += category.night_rate

    return fee, rate_type

    def __str__(self):
        return f"{self.plate_number} ({self.ticket_number})"
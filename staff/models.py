from django.db import models
from django.contrib.auth.models import AbstractUser


class Staff(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('ATTENDANT', 'Attendant'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='ADMIN'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
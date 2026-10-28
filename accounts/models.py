from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        DOCTOR = 'DOCTOR', 'Doctor'
        PATIENT = 'PATIENT', 'Patient'
        ADMIN = 'ADMIN', 'Admin'
        
    base_role = Role.PATIENT
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    
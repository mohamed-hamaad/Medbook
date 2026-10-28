from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    development_stage = models.CharField(max_length=100, help_text="e.g., Fully Advanced, Under Development")
    image = models.ImageField(upload_to='departments/', blank=True, null=True)
    
    def get_doctors_count(self):
        return self.doctors.count() 

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'DOCTOR'}, related_name='doctor_profile') 
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Doctor's direct contact number")
    bio = models.TextField(blank=True)
    available_days = models.CharField(max_length=100, help_text="e.g., Mon-Fri, Sat-Sun", default="N/A")
    available_time = models.CharField(max_length=100, help_text="e.g., 9:00 AM - 5:00 PM", default="N/A")
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    is_available_today = models.BooleanField(default=True, help_text="Is the doctor active in the clinic right now?")

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} - {self.department.name if self.department else 'No Department'}"


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('INVESTIGATING', 'Under Investigation'),
        ('RESOLVED', 'Resolved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Complaint: {self.subject} ({self.get_status_display()})"
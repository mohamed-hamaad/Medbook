
from django.db import models
from django.conf import settings
from clinics.models import DoctorProfile
# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50)
    patient_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    queue_number = models.PositiveIntegerField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.queue_number:
            current_depar = self.doctor.department
            existing_count = Appointment.objects.filter(
                doctor__department=current_depar,
                appointment_date=self.appointment_date
            ).count()
            self.queue_number = existing_count + 1
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dept Order #{self.queue_number} in {self.doctor.department.name}"
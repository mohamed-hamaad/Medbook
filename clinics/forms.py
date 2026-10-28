from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import DoctorProfile

class EditDoctorProfileForm (forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = fields = ['department', 'phone_number', 'bio', 'available_days', 'available_time', 'profile_picture', 'experience_years', 'consultation_fee', 'is_available_today']

    def __init__(self, *args, **kwargs):
        super(EditDoctorProfileForm, self).__init__(*args, **kwargs)
        if 'department' in self.fields:
            self.fields['department'].disabled= True

        self.fields['experience_years'].disabled= True

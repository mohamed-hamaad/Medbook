from django.urls import path
from .views import *

urlpatterns = [
    path('clinics/home/', home, name='clinics_home'), 
    path('department/<int:department_id>/', department_detail, name='department_detail'),
    path('doctor/<int:doctor_id>/', doctor_profile, name='doctor_profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('appointment/<int:appt_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:appt_id>/confirm/', confirm_appointment, name='confirm_appointment'),
    
]
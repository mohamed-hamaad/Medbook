from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clinics.models import DoctorProfile
from .models import Appointment

@login_required
def book_clinic(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    return render(request, 'bookings/book_clinic.html', {'doctor': doctor})

@login_required
def finish_booking(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')
        patient_notes = request.POST.get('patient_notes', '')
        
        if selected_date and selected_time:
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=selected_date,
                appointment_time=selected_time,
                patient_notes=patient_notes,
                status='PENDING'
            )
            return render(request, 'bookings/booking_success.html', {'appointment': appointment})
        else:
            return redirect('book_clinic', doctor_id=doctor.id)

    date = request.GET.get('date')
    time = request.GET.get('time')
    
    context = {
        'doctor': doctor,
        'date': date,
        'time': time,
    }
    return render(request, 'bookings/finish_booking.html', context)
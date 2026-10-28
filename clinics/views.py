from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from .models import *
from .filters import DepartmentFilter
from bookings.models import Appointment
from .models import Department
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from .forms import EditDoctorProfileForm
from django.utils import timezone
from datetime import timedelta
def home(request):
    queryset = Department.objects.all().order_by('name')
    dept_filter = DepartmentFilter(request.GET, queryset=queryset)
    filtered_queryset = dept_filter.qs
    paginator = Paginator(filtered_queryset, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': dept_filter,
        'page_obj': page_obj, 
    }
    return render(request, 'clinics/home.html', context)

def department_detail(request, department_id):
    department = Department.objects.get(id=department_id)
    doctors = department.doctors.all() 
    return render(request, 'clinics/department_detail.html', {'department': department, 'doctors': doctors})

def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    form = None
    
    if request.user.is_authenticated and request.user == doctor.user:
        if request.method == 'POST':
            form = EditDoctorProfileForm(request.POST, request.FILES, instance=doctor)
            if form.is_valid():
                form.save()
                return redirect('doctor_profile', doctor_id=doctor.id)
        else:
            form = EditDoctorProfileForm(instance=doctor)
            
    return render(request, 'clinics/doctor_profile.html', {
        'doctor': doctor,
        'form': form 
    })
@login_required
def dashboard(request):
    user = request.user
    search_query = request.GET.get('search', '').strip() 

    # 1. Doctor Dashboard
    if user.role == 'DOCTOR':
        appointments = Appointment.objects.filter(doctor__user=user).exclude(status='CANCELLED').order_by('appointment_date', 'appointment_time')
        if search_query:
            appointments = appointments.filter(
                Q(patient__username__icontains=search_query) | 
                Q(patient__first_name__icontains=search_query) | 
                Q(patient__last_name__icontains=search_query)
            )
            
        return render(request, 'clinics/dashboards/doctor_dashboard.html', {
            'appointments': appointments, 
            'search_query': search_query
        })
        
    # 2. Admin/Staff Dashboard
    elif user.role == 'ADMIN' or user.is_staff:
        last_week = timezone.now().date() - timedelta(days=7)
        complaints = Complaint.objects.all().select_related('user').order_by('-created_at')
        
        if search_query:
            departments = Department.objects.prefetch_related(
                Prefetch(
                    'doctors__appointments',
                    queryset=Appointment.objects.filter(
                        Q(patient__username__icontains=search_query) |
                        Q(doctor__user__last_name__icontains=search_query)
                    ).select_related('patient', 'doctor__user').order_by('appointment_date', 'appointment_time')
                )
            ).all()
            
            complaints = complaints.filter(
                Q(subject__icontains=search_query) | 
                Q(user__username__icontains=search_query)
            )
            
        else:
            departments = Department.objects.prefetch_related(
                Prefetch(
                    'doctors__appointments',
                    queryset=Appointment.objects.filter(appointment_date__gte=last_week).select_related('patient').order_by('appointment_date', 'appointment_time')
                )
            ).all()
            
        return render(request, 'clinics/dashboards/admin_dashboard.html', {
            'departments': departments, 
            'complaints': complaints,
            'search_query': search_query
        })

    # 3. Patient Dashboard
    else:
        if request.method == "POST" and "submit_complaint" in request.POST:
            subject = request.POST.get("subject")
            message = request.POST.get("message")
        
            if subject and message:
                Complaint.objects.create(
                    user=request.user,
                    subject=subject,
                    message=message
                )
                return redirect('dashboard')
        appointments = Appointment.objects.filter(patient=user).order_by('-appointment_date')
        return render(request, 'clinics/dashboards/patient_dashboard.html', {'appointments': appointments, 'search_query': search_query})


#managing appointments

@login_required
def cancel_appointment(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)
    
    is_patient = request.user == appt.patient
    is_doctor = appt.doctor.user == request.user
    
    if is_patient or is_doctor:
        appt.status = 'CANCELLED'
        appt.save()
        
    return redirect('dashboard')


@login_required
def confirm_appointment(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)
    
    if appt.doctor.user == request.user:
        appt.status = 'CONFIRMED'
        appt.save()
        
    return redirect('doctor_dashboard')


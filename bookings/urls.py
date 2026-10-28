from django.urls import path
from .views import book_clinic, finish_booking

urlpatterns = [
    path('doctor/<int:doctor_id>/book/', book_clinic, name='book_clinic'),
    path('doctor/<int:doctor_id>/finish/', finish_booking, name='finish_booking'),
]
from django.urls import path, include

from .views import get_bookings, create_booking

urlpatterns=[
    path('', get_bookings, name='get_bookings'),
    path('create-booking/', create_booking, name='create-booking')
]
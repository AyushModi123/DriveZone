from django.urls import path
from . import views

urlpatterns = [
    path('',  views.SlotView.as_view(), name='slots'),
    path('<int:inst_id>/', views.get_available_instructor_slots, name='available_slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('booked/', views.get_booked_slots, name='booked_slot'),
]
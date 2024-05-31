from django.urls import path
from . import views

urlpatterns = [
    path('create/',  views.create_slot, name='create_slot'),
    path('available-slots/', views.get_slots, name='available_slots'),
]
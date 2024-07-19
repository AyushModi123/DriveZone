from django.urls import path
from . import views

urlpatterns = [
    path('',  views.SlotView.as_view(), name='slots'),
    path('<int:inst_id>/', views.get_available_instructor_slots, name='available_slots'),
    path('<int:slot_id>/', views.book_slot, name='book_slot')
]
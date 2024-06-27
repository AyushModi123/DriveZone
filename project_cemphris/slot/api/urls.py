from django.urls import path
from . import views

urlpatterns = [
    path('',  views.SlotView.as_view(), name='slots'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',  views.check_api),
    path('signup/', views.signup, name='signup')
]
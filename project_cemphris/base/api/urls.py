from django.urls import path
from . import views

urlpatterns = [
    path('',  views.check_api),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account')
]
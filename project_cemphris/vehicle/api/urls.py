from django.urls import path
from . import views

urlpatterns=[
    path('', views.VehicleView.as_view(), name='vehicles'),
    path('vehicle/', views.get_vehicle, name='get_vehicle'),
    path('upload-image/', views.upload_image, name='upload_vehicle_image')
]
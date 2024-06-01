from django.urls import path
from . import views

urlpatterns=[
    path('create/', views.create_vehicle, name='create_vehicle'),
    path('vehicle/', views.get_vehicle, name='get_vehicle'),
    path('upload-image/', views.upload_image, name='upload_vehicle_image')
]
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', viewset=views.VehicleViewSet, basename="")

urlpatterns=[
    path('', views.VehicleViewSet, name='vehicles'),
    # path('vehicle/', views.get_vehicle, name='get_vehicle'),
    path('upload-image/', views.upload_image, name='upload_vehicle_image')
]

urlpatterns+=router.urls
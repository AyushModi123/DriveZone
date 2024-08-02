from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', viewset=views.ReviewViewSet, basename="")

urlpatterns=[
]

urlpatterns+=router.urls
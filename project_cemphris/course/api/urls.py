from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', viewset=views.CourseViewSet, basename="")
router.register(r'enroll', viewset=views.EnrollCourseViewSet, basename="enroll")

urlpatterns = [
]

urlpatterns+=router.urls
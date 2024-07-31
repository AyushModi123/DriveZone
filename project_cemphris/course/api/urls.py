from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', viewset=views.CourseViewSet, basename="")
urlpatterns = [
    path('enroll/<int:pk>/assign-instructor/', views.assign_instructor, name='assign_instructor'),
    path('enroll/', views.get_enrollment, name='get_enrollments'),
]

urlpatterns+=router.urls
"""
URL configuration for project_cemphris project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


schema_view = get_schema_view(
    openapi.Info(
        title="Project Cemphris Title",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
    authentication_classes=[SessionAuthentication],
)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/users/', include('base.api.urls')),
    path('api/auth/', include('jwt_auth.urls')),
    # path('api/bookings/', include('booking.api.urls')),
    path('api/slots/', include('slot.api.urls')),
    path('api/vehicles/', include('vehicle.api.urls')),
    path('api/review/', include('review.api.urls')),
    path('api/courses/', include('course.api.urls')),
    path('api/payments/', include('payment.api.urls')),
]

#Swagger Docs
urlpatterns+= [    
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]
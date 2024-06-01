from django.urls import path
from . import views

urlpatterns=[
    path('rate/', views.rate_instructor),
    path('get-rating/', views.get_rating),
]
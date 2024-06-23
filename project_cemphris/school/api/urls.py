from django.urls import path
from . import views

urlpatterns=[
    path('create/', view=views.create_school),
    # path('', view=views.get_details),
    # path('update/', view=views.update_details),
    path('upload-image/', views.upload_image, name='upload_school_image'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',  views.check_api),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('upload-image/', views.upload_image, name='upload_profile_image'),
    path('details/', views.get_user_details, name='get_user_details'),
    path('create-school/', views.create_school, name='create-school'),
    path('create-learner/', views.create_learner, name='create-learner'),
    path('upload-license/', views.upload_license, name='upload-license'),
    path('instructors/', views.InstructorView.as_view(), name='instructors')
    # path('update-details/', views.update_details, name='update_user_details'),
    # path('update-license/', views.update_license, name='update_license_details'),
]
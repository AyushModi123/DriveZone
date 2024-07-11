from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()

router.register(r'schools', viewset=views.SchoolViewSet, basename="schools")


urlpatterns = [
    path('',  views.check_api),
    path('signup/', views.signup, name='signup'),
    path('send-activation-mail/', views.resend_activation_mail, name='send_activation_mail'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('upload-image/', views.upload_image, name='upload_profile_image'),
    path('details/', views.get_user_details, name='get_user_details'),
    path('create-school/', views.create_school, name='create-school'),
    path('create-learner/', views.create_learner, name='create-learner'),
    path('upload-license/', views.upload_license, name='upload-license'),
    path('instructors/', views.InstructorView.as_view(), name='instructors'),
    path("password-reset/", views.password_reset, name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/", views.PasswordReset.as_view(), 
        name="password_reset_confirm",
    ),
    # path(
    #     "password-reset-complete/",
    #     auth_views.PasswordResetCompleteView.as_view(
    #         template_name="base/password_reset_complete.html"
    #     ),
    #     name="password_reset_complete",
    # ),
    # path('update-details/', views.update_details, name='update_user_details'),
    # path('update-license/', views.update_license, name='update_license_details'),
]

urlpatterns+=router.urls
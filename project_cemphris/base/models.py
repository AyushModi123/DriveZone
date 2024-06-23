from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from vehicle.models import VehicleChoices
from .choices import ProfileCompletionLevelChoices, LicenseIssuingAuthorityChoices, LicenseTypeChoices
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):    
    username = None
    profile_completion_level = models.IntegerField(choices=ProfileCompletionLevelChoices.choices, null=False, blank=False, default=1)
    email = models.EmailField(unique=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_learner(self):
        try:
            return bool(self.learner)
        except ObjectDoesNotExist:
            return False
    
    @property
    def is_school(self):
        try:
            return bool(self.school)
        except ObjectDoesNotExist:
            return False
    
    @property
    def is_instructor(self):
        try:
            return bool(self.instructor)
        except ObjectDoesNotExist:
            return False
    
    @property
    def check_license(self):
        try:
            return bool(self.license)
        except ObjectDoesNotExist:
            return False
        


class Learner(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='learner')    
    full_name = models.CharField(max_length=255, blank=False, null=False, default="XYZ")    
    location = models.CharField(max_length=2000, null=True, blank=True)
    image_url = models.URLField(null=False, blank=True, default='')    
    mobile_number = models.CharField(max_length=20, null=True, blank=False, default="0000000000")
    preferred_language = models.CharField(null=True, blank=False, default='English')

    def __str__(self):
        return self.full_name


class Instructor(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='instructor')
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='instructors')
    full_name = models.CharField(max_length=255, blank=False, null=False, default="XYZ")
    experience = models.IntegerField(null=True, blank=False, default=0)
    area_of_expertise = models.IntegerField(choices=VehicleChoices.choices, null=True, blank=False)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True, blank=False, related_name='instructors')

    def __str__(self):
        return self.full_name
    

class LicenseInformation(models.Model):    
    
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='license')
    number = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    # photo
    image_url = models.URLField(null=False, blank=True, default='')
    type = models.IntegerField(choices=LicenseTypeChoices.choices, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    issuing_authority = models.IntegerField(choices=LicenseIssuingAuthorityChoices.choices, blank=False, null=False)

#plans
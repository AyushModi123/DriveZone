from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from vehicle.models import VehicleChoices
from .choices import ProfileCompletionLevelChoices, LicenseIssuingAuthorityChoices, LicenseTypeChoices, RoleChoices


class User(AbstractUser):    
    username = models.CharField(null=False, blank=True, unique=False, default="")
    profile_completion_level = models.IntegerField(choices=ProfileCompletionLevelChoices.choices, null=False, blank=False, default=1)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.LEARNER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_learner(self):
        if self.role == RoleChoices.LEARNER:
            return True
        return False
    
    @property
    def is_school(self):
        if self.role == RoleChoices.SCHOOL:
            return True
        return False
    
    @property
    def is_instructor(self):
        if self.role == RoleChoices.INSTRUCTOR:
            return True
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
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=False, related_name='instructors')
    full_name = models.CharField(max_length=255, blank=False, null=False, default="XYZ")
    location = models.CharField(max_length=2000, null=True, blank=True)
    image_url = models.URLField(null=False, blank=True, default='')    
    mobile_number = models.CharField(max_length=20, null=True, blank=False, default="0000000000")
    preferred_language = models.CharField(null=True, blank=False, default='English')
    experience = models.IntegerField(null=True, blank=False, default=0)
    area_of_expertise = models.IntegerField(choices=VehicleChoices.choices, null=True, blank=False)

    def __str__(self):
        return self.full_name
    
class School(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='school')
    name = models.CharField(max_length=500, blank=False, null=False)    
    location = models.CharField(max_length=2000, null=True, blank=True)
    image_url = models.URLField(null=False, blank=True, default='')
    mobile_number = models.CharField(max_length=20, null=True, blank=False, default="0000000000")
    preferred_language = models.CharField(null=True, blank=False, default='English')    

    def __str__(self):
        return self.name

class LicenseInformation(models.Model):    
    
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='license')
    number = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    # photo
    image_url = models.URLField(null=False, blank=True, default='')
    type = models.IntegerField(choices=LicenseTypeChoices.choices, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    issuing_authority = models.IntegerField(choices=LicenseIssuingAuthorityChoices.choices, blank=False, null=False)

#plans
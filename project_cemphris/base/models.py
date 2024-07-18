from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.validators import MaxValueValidator
from vehicle.models import VehicleChoices
from .choices import ProfileCompletionLevelChoices, LicenseIssuingAuthorityChoices, LicenseTypeChoices, RoleChoices


class User(AbstractUser):    
    username = models.CharField(null=False, blank=True, unique=False, default="")
    profile_completion_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], null=False, blank=False, default=10)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    role = models.CharField(max_length=50, choices=RoleChoices.choices, null=False, blank=False)
    # TODO: set role as editable false later
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
        
    @property
    def get_role_model(self):
        if self.is_learner:
            return self.learner
        elif self.is_instructor:
            return self.instructor
        elif self.is_school:
            return self.school
        else:
            return None    

    @property
    def has_any_notifications(self):
        try:
            return bool(self.notifications)
        except ObjectDoesNotExist:
            return False

class Learner(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='learner', null=False, blank=False)
    full_name = models.CharField(max_length=255, blank=False, null=False)    
    location = models.CharField(max_length=2000, null=True, blank=False)
    image_url = models.URLField(null=False, blank=True, default='')    
    mobile_number = models.CharField(max_length=20, null=True, blank=False)
    preferred_language = models.CharField(null=True, blank=False, default='English')

    def __str__(self):
        return self.full_name

    @property
    def get_profile_fields(self):
        """Returns fields that 
        contribute to profile completion level in format
        {'location': [fields]}
        full_name, location, image_url, mobile_number, preferred_language, license
        """

        return {"current": ["full_name", "location", "image_url", "mobile_number", "preferred_language"], 
                "user": ["license"]
                }, 6
    #Update logic here
    @property
    def get_completion_level(self):
        """This property directly depends on get_profile_fields property"""
        temp, total_fields = self.get_profile_fields
        empty_fields = 0.0
        for field in temp["current"]:
            value = getattr(self, field)
            if value in [None, '', [], {}]:
                empty_fields += 1
        for field in temp["user"]:
            if not hasattr(self.user, field):
                empty_fields+=1
        non_empty_fields = total_fields - empty_fields
        return (non_empty_fields/total_fields)*100
    
    @property
    def get_course(self):
        try:
            return self.course
        except ObjectDoesNotExist:
            return None

class Instructor(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='instructor', null=False, blank=False)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=False, blank=False, related_name='instructors')
    full_name = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=2000, null=True, blank=False)
    image_url = models.URLField(null=False, blank=True, default='')    
    mobile_number = models.CharField(max_length=20, null=True, blank=False)
    preferred_language = models.CharField(null=True, blank=False, default='English')
    experience = models.IntegerField(null=True, blank=False, default=0)
    area_of_expertise = models.CharField(choices=VehicleChoices.choices, null=False, blank=False)

    def __str__(self):
        return self.full_name
    
    @property
    def get_profile_fields(self):
        """Returns fields that 
        contribute to profile completion level in format
        {'location': [fields]}
        full_name, location, image_url, mobile_number, preferred_language, license, experience, area_of_expertise
        """

        return {"current": ["full_name", "location", "image_url", "mobile_number", "preferred_language", "experience", "area_of_expertise"], 
                "user": ["license"]
                }, 8
    @property
    def get_completion_level(self):
        """This property directly depends on get_profile_fields property"""
        temp, total_fields = self.get_profile_fields
        empty_fields = 0.0
        for field in temp["current"]:
            value = getattr(self, field)
            if value in [None, '', [], {}]:
                empty_fields += 1
        for field in temp["user"]:
            if not hasattr(self.user, field):
                empty_fields+=1
        non_empty_fields = total_fields - empty_fields
        return (non_empty_fields/total_fields)*100
    
    
class School(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='school')
    name = models.CharField(max_length=500, blank=False, null=False)
    desc = models.TextField(blank=True, null=False, default="")
    location = models.CharField(max_length=2000, null=True, blank=True)
    image_url = models.URLField(null=False, blank=True, default='')
    mobile_number = models.CharField(max_length=20, null=True, blank=False)
    preferred_language = models.CharField(null=True, blank=False, default='English')    

    def __str__(self):
        return self.name

    @property
    def get_profile_fields(self):
        """Returns fields that 
        contribute to profile completion level in format
        {'location': [fields]}
        name, location, image_url, mobile_number, preferred_language
        """

        return {"current": 
                ["name", "location", "image_url", "mobile_number", "preferred_language"],  
                "vehicle": ["vehicles"]               
                }, 5
    @property
    def get_completion_level(self):
        """This property directly depends on get_profile_fields property"""
        temp, total_fields = self.get_profile_fields
        empty_fields = 0.0
        for field in temp["current"]:
            value = getattr(self, field)
            if value in [None, '', [], {}]:
                empty_fields += 1
        for field in temp["vehicle"]:
            if not hasattr(self, field):
                empty_fields+=1
        non_empty_fields = total_fields - empty_fields
        return (non_empty_fields/total_fields)*100

class LicenseInformation(models.Model):    
    
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='license')
    number = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    # photo
    image_url = models.URLField(null=False, blank=True, default='')
    type = models.CharField(choices=LicenseTypeChoices.choices, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    issuing_authority = models.CharField(choices=LicenseIssuingAuthorityChoices.choices, blank=False, null=False)

    def __str__(self):
        return self.number

class ActivationMailHistory(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    sent_count = models.SmallIntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.email} -> {self.sent_count}"
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=2000, null=True, blank=True)
    # avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_learner(self):
        try:
            return bool(self.learner)
        except ObjectDoesNotExist:
            return False
    
    @property
    def is_instructor(self):
        try:
            return bool(self.instructor)
        except ObjectDoesNotExist:
            return False

class Learner(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='learner')

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user: User = models.OneToOneField('User', on_delete=models.CASCADE, related_name='instructor')    

    def __str__(self):
        return self.user.username
    
    # class Meta:
    #     db_table = 'custom_slot_table'

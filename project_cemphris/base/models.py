from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=2000, null=True, blank=True)
    # avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Learner(models.Model):
    user: User  = models.OneToOneField('User', on_delete=models.CASCADE, related_name='learner')

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user: User = models.OneToOneField('User', on_delete=models.CASCADE, related_name='instructor')    

    def __str__(self):
        return self.user.username
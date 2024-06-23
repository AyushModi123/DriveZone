from django.db import models
# Create your models here.

class School(models.Model):
    user = models.OneToOneField('base.User', on_delete=models.CASCADE, related_name='school')
    name = models.CharField(max_length=500, blank=False, null=False)    
    location = models.CharField(max_length=2000, null=True, blank=True)
    image_url = models.URLField(null=False, blank=True, default='')
    mobile_number = models.CharField(max_length=20, null=True, blank=False, default="0000000000")
    preferred_language = models.CharField(null=True, blank=False, default='English')    

    def __str__(self):
        return self.name
    

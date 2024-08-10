from django.db import models
from .choices import VehicleChoices, VehicleTypeChoices

class Vehicle(models.Model):

    school = models.ForeignKey('base.School', on_delete=models.CASCADE, related_name='vehicles', default=1)
    image_url = models.URLField(null=False, blank=True, default='')
    model = models.CharField(max_length=50, null=False, blank=False, default='XXXXX')
    make = models.CharField(choices=VehicleChoices.choices, null=False, blank=False)
    type = models.CharField(choices=VehicleTypeChoices.choices, null=False, blank=False)
    plate_no = models.CharField(max_length=15, null=False, blank=False, default='XX000000')

    def __str__(self):
        return f"id: {self.id}->{self.get_make_display()} with model {self.model}"
    
    # class Meta:        
    #     constraints = [
    #         models.UniqueConstraint(fields=['plate_no'], name='unique_plate_no')
    #     ]
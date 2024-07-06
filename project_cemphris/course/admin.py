from django.contrib import admin
from .models import Course, EnrollCourse
# Register your models here.
admin.site.register(Course)
admin.site.register(EnrollCourse)
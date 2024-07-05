from django.contrib import admin
from .models import Course, LearnerCourse
# Register your models here.
admin.site.register(Course)
admin.site.register(LearnerCourse)
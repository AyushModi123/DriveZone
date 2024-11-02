from django.db import models

class CourseActivity(models.Model):
    enroll_detail = models.ForeignKey('course.EnrollCourse', on_delete=models.CASCADE, related_name='activities')
    work_update = models.CharField(max_length=1024,null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



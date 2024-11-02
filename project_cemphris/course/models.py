from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Course(models.Model):

    school = models.ForeignKey('base.School', on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=64, null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    course_content = models.JSONField(null=False, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "School: " + self.school.name + " with id: " + str(self.id)
    
    @property
    def get_enrolled(self):
        try:
            return self.learner_courses
        except ObjectDoesNotExist:
            return None
    
class EnrollCourse(models.Model):
    payment = models.OneToOneField('payment.PaymentDetail', on_delete=models.CASCADE, related_name='enroll')
    learner = models.OneToOneField('base.Learner', on_delete=models.CASCADE, related_name='learner_course')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='learner_courses')
    instructor = models.ForeignKey('base.Instructor', on_delete=models.CASCADE, null=True, blank=False, related_name='learner_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_instructor_assigned(self):
        try:
            return bool(self.instructor)
        except ObjectDoesNotExist:
            return False
    
    class EnrollmentNotFound(Exception):
        pass
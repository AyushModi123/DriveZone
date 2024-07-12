from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Course(models.Model):

    school = models.ForeignKey('base.School', on_delete=models.CASCADE, related_name='courses')
    course_content = models.JSONField(null=False, blank=False)

    def __str__(self):
        return "School: " + self.school.name + " with id: " + str(self.id)
    
class EnrollCourse(models.Model):
    payment = models.OneToOneField('payment.PaymentDetail', on_delete=models.CASCADE, related_name='enroll')
    learner = models.OneToOneField('base.Learner', on_delete=models.CASCADE, related_name='learner_course')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='learner_courses')
    instructor = models.ForeignKey('base.Instructor', on_delete=models.CASCADE, null=True, blank=False, related_name='learner_courses')    

    @property
    def is_instructor_assigned(self):
        try:
            return bool(self.instructor)
        except ObjectDoesNotExist:
            return False
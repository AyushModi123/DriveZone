from django.db import models

class Course(models.Model):

    school = models.ForeignKey('base.School', on_delete=models.CASCADE, related_name='courses')
    course_content = models.JSONField(null=False, blank=False)

    def __str__(self):
        return "School: " + self.school.name + " with id: " + str(self.id)
    
class LearnerCourse(models.Model):
    learner = models.OneToOneField('base.Learner', on_delete=models.CASCADE, related_name='course')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrolled')
    
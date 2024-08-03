from django.db import models

class RatingChoices(models.IntegerChoices):
    ONE_STAR = (1, "One Star") 
    TWO_STARS = (2, "Two Star")
    THREE_STARS = (3, "Three Star")
    FOUR_STARS = (4, "Four Star")
    FIVE_STARS = (5, "Five Star")

class Review(models.Model):
    school = models.ForeignKey('base.School', on_delete=models.CASCADE, related_name='reviews')
    learner = models.ForeignKey('base.Learner', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RatingChoices.choices, null=False, blank=False)
    content = models.CharField(max_length=10000, null=False, blank=True, default="")

    def __str__(self):
        return f"{self.school}'s Rating: {self.get_rating_display()}"

    class Meta:        
        constraints = [
            models.UniqueConstraint(fields=['school', 'learner'], name='one_learner_review_per_school')
        ]

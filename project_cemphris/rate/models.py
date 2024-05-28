from django.db import models

class RatingChoices(models.IntegerChoices):
    ONE_STAR = 1 
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

class Rating(models.Model):
    instructor = models.OneToOneField('base.instructor', on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(choices=RatingChoices.choices)

    def __str__(self):
        return f"{self.instructor}'s Rating: {self.rating}"


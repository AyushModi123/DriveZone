from rest_framework import serializers
from review.models import Review

class OutReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'school', 'rating', 'content')

    def get_rating(self, obj):
        """Called for make serializer field"""
        return obj.get_rating_display()
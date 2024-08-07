from rest_framework import serializers
from review.models import Review

class OutReviewSerializer(serializers.ModelSerializer):
    learner_name = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ('id', 'school', 'rating', 'content', 'learner')

    def get_rating(self, obj):
        """Called for make serializer field"""
        return obj.get_rating_display()

    def get_learner_name(self, obj):
        """Called for make serializer field"""
        return obj.learner.full_name
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('school', 'rating', 'content')
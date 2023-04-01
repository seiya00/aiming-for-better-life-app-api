"""
Serializers for the meal API View
"""
from rest_framework import serializers

from core.models import MealQuestion, MealUser


class MealQuestionSerializer(serializers.ModelSerializer):
    """Serializer for MealQuestion"""

    class Meta:
        model = MealQuestion
        fields = ['id',
                  'is_allergy',
                  'is_unnecessary',
                  'answer_type',
                  'answer_choice',
                  'answer_int',
                  'answer_bool'
        ]
        read_only_fields = ['id']


class MealUserSerializer(serializers.ModelSerializer):
    """Serializer for MealUser"""

    class Meta:
        model = MealUser
        fields = [
            'id',
            'is_allergy',
            'is_unnecessary',
            'answer_type',
            'answer_choice',
            'answer_int',
            'answer_bool'
        ]
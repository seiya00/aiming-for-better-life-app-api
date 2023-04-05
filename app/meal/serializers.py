"""
Serializers for the meal API View
"""
from rest_framework import serializers

from core.models import MealQuestion, MealUser


class MealQuestionSerializer(serializers.ModelSerializer):
    """Serializer for MealQuestion"""

    class Meta:
        model = MealQuestion
        fields = [
            'id',
            'question',
        ]

        read_only_fields = ['id']


class MealUserSerializer(serializers.ModelSerializer):
    """Serializer for MealUser"""

    meal_question=MealQuestionSerializer

    class Meta:
        model = MealUser
        fields = [
            'id',
            'meal_question',
            'vegetable_question',
            'answer_type',
            'answer_choice',
            'answer_int',
            'answer_bool',
        ]
        # fields = '__all__'

        read_only_fields = ['id']

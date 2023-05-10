"""
Serializers for question API View
"""
from rest_framework import serializers

from core.models import Questions


class QuestionsSerializer(serializers.ModelSerializer):
    """Serializer for Questions"""

    class Meta:
        model = Questions
        fields = [
            'id',
            'question',
            'question_type',
            'answer_type',
            'is_neccessary',
            'answer1_choice',
            'answer2_choice',
            'answer3_choice',
            'answer4_choice',
            'answer1_bool',
            'answer2_bool'
        ]

        read_only_fields = ['id']

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
            'answer1',
            'answer2',
            'answer3',
            'answer4'
        ]

        read_only_fields = ['id']

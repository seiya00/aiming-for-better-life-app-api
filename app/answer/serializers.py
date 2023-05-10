"""
Serializers for the answer API View
"""
from rest_framework import serializers

from core.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer"""

    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'vegetable',
            'answer_type',
            'answer_choice',
            'answer_int',
            'answer_bool',
            'created_at',
        ]

        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create a meal user"""
        answer = Answer.objects.create(**validated_data)
        return answer
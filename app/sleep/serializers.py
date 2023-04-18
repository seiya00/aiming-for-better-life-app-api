"""
Serializers for sleep API View
"""
from rest_framework import serializers

from core.models import (
    SleepQuestion,
    SleepUser
)


class SleepQuestionSerializer(serializers.ModelSerializer):
    """Serializer for SleepQuestion"""

    class Meta:
        model = SleepQuestion
        fields = [
            'id',
            'question',
        ]

        read_only_fields = ['id']


class SleepUserSerializer(serializers.ModelSerializer):
    """Serializer for SleepUser"""

    sleep_question = SleepQuestionSerializer

    class Meta:
        model = SleepUser
        fields = [
            'id',
            'sleep_question',
            'answer_type',
            'answer_choice',
            'answer_int',
            'answer_bool',
        ]

        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a sleep user"""
        sleep_user = SleepUser.objects.create(**validated_data)
        return sleep_user
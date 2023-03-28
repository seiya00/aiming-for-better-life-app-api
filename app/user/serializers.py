"""
Searizers for the user API View
"""
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'gender']
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 5,
                         'validators': [RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
                                                       message='Password must contain at least one single-byte lowercase, ' \
                                                               'upercase and numeric character. Total length should be more than 5 chars!')]},
            'email': {},
            'first_name': {},
            'last_name': {},
            'gender': {},
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

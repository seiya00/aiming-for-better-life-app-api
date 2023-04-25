"""
Searizers for the user API View
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'gender']
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 5,
                         'validators': [RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', # noqa
                                                       message='Password must contain at least one ' # noqa
                                                               'single-byte lowercase, upercase and numeric ' # noqa
                                                               'character. Total length should be more than 5 chars!')]} # noqa
        }
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attributes):
        """Validate and authenticate the user"""
        email = attributes.get('email')
        password = attributes.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attributes['user'] = user
        return attributes

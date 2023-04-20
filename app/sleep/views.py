"""
Views for sleep APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    SleepQuestion,
    SleepUser
)
from sleep import serializers


class SleepQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage sleep question APIs"""
    serializer_class = serializers.SleepQuestionSerializer
    queryset = SleepQuestion.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SleepUserViewSet(viewsets.ModelViewSet):
    """View for manage sleep user APIs"""
    serializer_class = serializers.SleepUserSerializer
    queryset = SleepUser.objects.all()
    http_method_names = ['get', 'post', 'patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve sleep user for autheticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, seiralizer):
        """Save data"""
        seiralizer.save(user=self.request.user)
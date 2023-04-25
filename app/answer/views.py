"""
Views for the answer APIs
"""
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Answer
from answer import serializers


class AnswerViewSet(viewsets.ModelViewSet):
    """View for manage meal user APIs"""
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.all()
    http_method_names = ['get', 'post', 'patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve meal user for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Save data"""
        serializer.save(user=self.request.user)

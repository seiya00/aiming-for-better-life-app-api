"""
Views for the question APIs
"""
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Questions
from question import serializers


class QuestionsViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage meal question APIs"""
    serializer_class = serializers.QuestionsSerializer
    queryset = Questions.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def list(self):
    #     """Retrieve meal question for authenticated user"""
    #     return self.queryset.order_by('-id')

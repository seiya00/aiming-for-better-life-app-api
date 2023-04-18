"""
Views for sleep APIs
"""
from rest_framework import viewsets
from rest_framework.authetication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    SleepQuestion,
    SleepUser
)
from sleep import seiralizers


class SleepQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage sleep question APIs"""
    serializer_class = seiralizers.SleepQuestionSerializer
    queryset = SleepQuestion.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

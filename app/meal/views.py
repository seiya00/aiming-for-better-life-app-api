"""
Views for the Meal APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import MealQuestion, MealUser
from meal import serializers


class MealQuestionViewSet(viewsets.ModelViewSet):
    """View for manage meal question APIs"""
    serializer_class = serializers.MealQuestionSerializer
    queryset = MealQuestion.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve meal question for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
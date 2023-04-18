"""
Views for the Meal APIs
"""
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import MealQuestion, MealUser
from meal import serializers


class MealQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage meal question APIs"""
    serializer_class = serializers.MealQuestionSerializer
    queryset = MealQuestion.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def list(self):
    #     """Retrieve meal question for authenticated user"""
    #     return self.queryset.order_by('-id')


class MealUserViewSet(viewsets.ModelViewSet):
    """View for manage meal user APIs"""
    serializer_class = serializers.MealUserSerializer
    queryset = MealUser.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve meal user for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Save data"""
        serializer.save(user=self.request.user)

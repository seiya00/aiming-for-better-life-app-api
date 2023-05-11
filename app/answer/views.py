"""
Views for the answer APIs
"""
from rest_framework import viewsets, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from core.models import Answer, Questions
from answer import serializers
from datetime import date, timedelta

def is_user_has_already_answered_the_question_today(user, question_id):
    today = date.today()
    return Answer.objects.filter(user=user, question__id=question_id, created_at=today).exists()


class AnswerViewSet(viewsets.ModelViewSet):
    """View for manage meal user APIs"""
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.all()
    http_method_names = ['get', 'post', 'patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        question_id = self.request.data.get('question', None)
        if question_id is not None:
            question = get_object_or_404(Questions, pk=question_id)
            if is_user_has_already_answered_the_question_today(user, question_id):
                return JsonResponse({'error': 'You can only answer the question once per day'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, question=question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid request. question_id is missing.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def yesterday(self, request, *args, **kwargs):
        """Filter data to retrieve only yesterday's data"""
        queryset = self.get_queryset().filter(created_at=date.today() - timedelta(days=1))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def week(self, request, *args, **kwargs):
        # 一週間分のデータをフィルタリングするロジック
        today = date.today()
        one_week_age = today - timedelta(days=7)
        meal_questions = self.get_queryset().filter(question__question_type='食事', created_at__range=(one_week_age, today))
        serializer = self.get_serializer(meal_questions, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Save data"""
        serializer.save(user=self.request.user)

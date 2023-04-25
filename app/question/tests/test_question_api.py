"""
Test for question APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Questions

from question.serializers import QuestionsSerializer


QUESTIONS_URL = reverse('question:questions-list')

def create_question(question):
    """Create and return a sample meal question"""
    question = Questions.objects.create(
        question=question
    )
    return question

class PublicAnswerAPITests(TestCase):
    """Test unautheticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(QUESTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAnswerAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        # You need to provide first_name, last_name etc...
        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='userPass123',
            first_name='test',
            gender='female'
        )
        self.client.force_authenticate(self.user)
        self.question1 = create_question('ついつい食べ過ぎてしまいますか？')
        self.question2 = create_question('昨日は魚をどれくらい食べましたか？')

    def test_retrieve_question(self):
        """Test retrieving meal question"""
        res = self.client.get(QUESTIONS_URL)

        questions = Questions.objects.all().order_by('-id')
        serializer = QuestionsSerializer(questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

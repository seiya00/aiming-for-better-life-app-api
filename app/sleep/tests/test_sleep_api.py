"""
Tests for sleep APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    SleepQuestion,
    SleepUser
)

from sleep.serializers import (
    SleepQuestionSerializer,
    SleepUserSerializer
)

SLEEP_QUESTION_URL = reverse('sleep:sleepquestion-list')
SLEEP_USER_URL = reverse('sleep:sleepuser-list')

def create_sleep_user(user, sleep_question, answer_type, answer_choice, answer_int, answer_bool):
    """Create and return a smaple sleep user"""
    sleep_user = SleepUser.objects.create(
        user=user,
        sleep_question=sleep_question,
        answer_type=answer_type,
        answer_choice=answer_choice,
        answer_int=answer_int,
        answer_bool=answer_bool
    )
    return sleep_user

def create_sleep_question(question):
    sleep_question = SleepQuestion.objects.create(
        question=question
    )
    return sleep_question

class PublicSleepAPITests(TestCase):
    """Test unautheticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(SLEEP_QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSleepAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='userPass123',
            first_name='test',
            last_name='taro',
            gender='female'
        )
        self.client.force_authenticate(self.user)
        self.sleep_question1 = create_sleep_question('目覚めた時の気分は？')
        self.sleep_user1 = create_sleep_user(
            user=self.user,
            sleep_question=self.sleep_question1,
            answer_type='choice',
            answer_choice='good',
            answer_int=None,
            answer_bool=None
        )

    def test_retrieve_sleep_question(self):
        """Test retrieving sleep question"""
        res = self.client.get(SLEEP_QUESTION_URL)

        sleep_questions = SleepQuestion.objects.all().order_by('-id')
        serializer = SleepQuestionSerializer(sleep_questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_correct_sleep_user(self):
        """Test retrieving sleep user"""
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='otherPass123',
            first_name='test',
            last_name='taro',
            gender='male'
        )
        create_sleep_user(
            user=other_user,
            sleep_question=self.sleep_question1,
            answer_type='choice',
            answer_choice='bad',
            answer_int=None,
            answer_bool=None
        )

        res = self.client.get(SLEEP_USER_URL)

        sleep_user = SleepUser.objects.filter(user=self.user)
        serializer = SleepUserSerializer(sleep_user, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_sleep_user(self):
        """Test creating sleep user"""
        payload = {
            'sleep_question': self.sleep_question1.id,
            'answer_type': 'choice',
            'answer_choice': 'excellent',
            'answer_int': None,
            'answer_bool': None
        }
        res = self.client.post(SLEEP_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        sleep_user = SL

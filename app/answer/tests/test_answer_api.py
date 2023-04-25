"""
Tests for answer APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Answer

from answer.serializers import AnswerSerializer

from question.serializers import QuestionsSerializer

QUESTION_URL = reverse('question:questions-list')
ANSWER_URL = reverse('answer:answer-list')

def answer_detail_url(answer_id):
    """Create and return a MealUser URL"""
    return reverse('answer:answer-detail', args=[answer_id])

def create_answer(user, question, vegetable, answer_type, answer_choice, answer_int, answer_bool):
    """Create and return a sample meal user"""
    answer = Answer.objects.create(
        user=user,
        question=question,
        vegetable=vegetable,
        answer_type=answer_type,
        answer_choice=answer_choice,
        answer_int=answer_int,
        answer_bool=answer_bool
    )
    return answer


class PublicAnswerAPITests(TestCase):
    """Test unautheticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(ANSWER_URL)

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
            gender='女性'
        )
        self.client.force_authenticate(self.user)
        self.res = self.client.get(QUESTION_URL)
        print(self.res.data)

    def test_retrieve_correct_answer(self):
        """Test retrieving meal user"""
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='otherPass123',
            first_name='test',
            gender='男性'
        )
        create_answer(
            user=other_user,
            question=self.res.data[0]['id'],
            vegetable=None,
            answer_type='choice',
            answer_choice='none',
            answer_int=None,
            answer_bool=None
        )

        res = self.client.get(ANSWER_URL)

        answer = Answer.objects.filter(user=self.user)
        serializer = AnswerSerializer(answer, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_answer(self):
        """Test creating meal user"""
        payload = {
            # 'user': self.user.id,
            'question': self.res.data[0]['id'],
            'vegetable': None,
            'answer_type': 'boolean',
            'answer_choice': None,
            'answer_int': None,
            'answer_bool': False
        }
        res = self.client.post(ANSWER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        answer = Answer.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if not k == 'question':
                self.assertEqual(getattr(answer, k), v)
            else:
                self.assertEqual(getattr(answer, k), self.question2)
        self.assertEqual(answer.user, self.user)

    def test_partial_update_answer(self):
        """Test partial update of a Answer"""
        payload = {
            'answer_bool': False
        }
        url = answer_detail_url(self.answer1.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.answer1.refresh_from_db()
        self.assertEqual(self.answer1.answer_bool, payload['answer_bool'])
        self.assertEqual(self.answer1.question, self.question1)
        self.assertEqual(self.answer1.user, self.user)
        self.assertEqual(self.answer1.answer_type, 'boolean')

    def test_update_user_returns_error(self):
        """Test changing the user in Answer results in error"""
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            password="otherPass123",
            first_name="other",
            gender="男性"
        )

        payload = {'user': other_user.id}
        url = answer_detail_url(self.answer1.id)
        self.client.patch(url, payload)

        self.answer1.refresh_from_db()
        self.assertEqual(self.answer1.user, self.user)


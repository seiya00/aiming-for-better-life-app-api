"""
Tests for meal APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MealUser
from core.models import MealQuestion

from meal.serializers import MealQuestionSerializer
from meal.serializers import MealUserSerializer

import json

MEAL_QUESTION_URL = reverse('meal:mealquestion-list')
MEAL_USER_URL = reverse('meal:mealuser-list')

def detail_url(meal_user_id):
    """Create and return a MealUser URL"""
    return reverse('meal:mealuser-detail', args=[meal_user_id])

def create_meal_user(user, meal_question, vegetable_question, answer_type, answer_choice, answer_int, answer_bool):
    """Create and return a sample meal user"""
    meal_user = MealUser.objects.create(
        user=user,
        meal_question=meal_question,
        vegetable_question=vegetable_question,
        answer_type=answer_type,
        answer_choice=answer_choice,
        answer_int=answer_int,
        answer_bool=answer_bool
    )
    return meal_user

def create_meal_question(question):
    """Create and return a sample meal question"""
    meal_question = MealQuestion.objects.create(
        question=question
    )
    return meal_question

class PublicMealAPITests(TestCase):
    """Test unautheticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(MEAL_QUESTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMealAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        # You need to provide first_name, last_name etc...
        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='userPass123',
            first_name='test',
            last_name='taro',
            gender='female'
        )
        self.client.force_authenticate(self.user)
        self.meal_question1 = create_meal_question('ついつい食べ過ぎてしまいますか？')
        self.meal_question2 = create_meal_question('昨日は魚をどれくらい食べましたか？')
        self.meal_user1 = create_meal_user(
            user=self.user,
            meal_question=self.meal_question1,
            vegetable_question=None,
            answer_type='boolean',
            answer_choice=None,
            answer_int=None,
            answer_bool=True
        )

    def test_retrieve_meal_question(self):
        """Test retrieving meal question one by one"""
        res = self.client.get(MEAL_QUESTION_URL)

        meal_questions = MealQuestion.objects.all().order_by('-id')
        serializer = MealQuestionSerializer(meal_questions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_correct_meal_user(self):
        """Test retrieving meal user"""
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='otherPass123',
            first_name='test',
            last_name='taro',
            gender='male'
        )
        create_meal_user(
            user=other_user,
            meal_question=self.meal_question2,
            vegetable_question=None,
            answer_type='choice',
            answer_choice='none',
            answer_int=None,
            answer_bool=None
        )

        res = self.client.get(MEAL_USER_URL)

        meal_by_user = MealUser.objects.filter(user=self.user)
        serializer = MealUserSerializer(meal_by_user, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_meal_user(self):
        """Test creating meal user"""
        payload = {
            # 'user': self.user.id,
            'meal_question': self.meal_question2.id,
            'vegetable_question': None,
            'answer_type': 'boolean',
            'answer_choice': None,
            'answer_int': None,
            'answer_bool': False
        }
        res = self.client.post(MEAL_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        meal_user = MealUser.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if not k == 'meal_question':
                self.assertEqual(getattr(meal_user, k), v)
            else:
                self.assertEqual(getattr(meal_user, k), self.meal_question2)
        self.assertEqual(meal_user.user, self.user)

    def test_partial_update(self):
        """Test partial update of a mealUser"""
        payload = {
            'answer_bool': False
        }
        url = detail_url(self.meal_user1.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.meal_user1.refresh_from_db()
        self.assertEqual(self.meal_user1.answer_bool, payload['answer_bool'])
        self.assertEqual(self.meal_user1.meal_question, self.meal_question1)
        self.assertEqual(self.meal_user1.user, self.user)
        self.assertEqual(self.meal_user1.answer_type, 'boolean')

    def test_update_user_returns_error(self):
        """Test changing the user in mealUser results in error"""
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            password="otherPass123",
            first_name="other",
            last_name="taro",
            gender="male"
        )

        payload = {'user': other_user.id}
        url = detail_url(self.meal_user1.id)
        self.client.patch(url, payload)

        self.meal_user1.refresh_from_db()
        self.assertEqual(self.meal_user1.user, self.user)


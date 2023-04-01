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

MEAL_QUESTION_URL = reverse('meal:meal-question')
MEAL_USER_URL = reverse('meal:meal-user')

def create_user_meal(user, meal_quesion, **params):
    """Create and return a sample meal"""
    # defaults = {
    #     'anser_type': 'choice',
    #     'anser_choice': 'a lot'
    # }
    # defaults.update(params)

    user_meal = MealUser.objects.create(user=user, meal_quesion=meal_quesion, **params)
    return user_meal

def create_meal_question(question):
    """Create and return a smaple meal question"""
    meal_question = MealQuestion.objects.create(question=question)
    return meal_question


class PublicMealAPITests(TestCase):
    """Test unautheticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(MEAL_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMealAPITests(TestCase):
    """Test authenticated API requests"""

    def test_retrieve_meal_question(self):
        """Test retrieving meal question one by one"""
        create_meal_question(question='ついつい食べ過ぎてしまいますか？')

        res = self.client.get(MEAL_QUESTION_URL)

        meal_question = MealQuestion.objects.all().first()
        serializer = MealQuestionSerializer(meal_question)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def setUp(self):
        self.client = APIClient()
        self.meal_question = MealQuestion.objects.create(
            question='揚げ物をどれくらい食べましたか？'
        )
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'Testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_meal_user(self):
        """Test retrieving meal user"""
        create_user_meal(
            user=self.user,
            meal_quesion=self.meal_question,
            answer_type='choice',
            answer_choice='none'
        )

        res = self.client.get(MEAL_USER_URL)

        meal_user = MealUser.objects.all().order_by('-id')
        serializer = MealUserSerializer(meal_user, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_meal_user_table_limited_to_correct_user(self):
        """Test MealUser object is limited to correct user"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'otherPass123'
        )
        create_user_meal(
            user=self.user,
            meal_quesion=self.meal_question,
            answer_type='choice',
            answer_choice='none'
        )
        create_user_meal(
            user=other_user,
            meal_quesion=self.meal_question,
            answer_type='choice',
            asnwer_choice='a lot'
        )

        res = self.client.get(MEAL_USER_URL)

        meal_user = MealUser.objects.filter(user=self.user)
        serializer = MealUserSerializer(meal_user, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)








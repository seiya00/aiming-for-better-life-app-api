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

MEAL_QUESTION_URL = reverse('meal:mealquestion-list')
MEAL_USER_URL = reverse('meal:mealuser-list')

def meal_user_url(meal_user_id):
    """Create and return a MealUser URL"""
    return reverse('meal:mealuser-list', args=[meal_user_id])

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
        self.user = get_user_model().objects.create_user(
            'user1@example.com',
            'Testpass123'
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
            answer_bool='True'
        )
        # self.meal_user2 = create_meal_user(
        #     user=self.user,
        #     meal_question=self.meal_question2,
        #     answer_type='choice',
        #     answer_choice='normal',
        #     answer_int=None,
        #     answer_bool=None
        # )

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
            'other1@example.com',
            'Otherpass123'
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

    # def test_meal_user_table_limited_to_correct_user(self):
    #     """Test MealUser object is limited to correct user"""
    #     other_user = get_user_model().objects.create_user(
    #         'other@example.com',
    #         'otherPass123'
    #     )
    #     create_meal_user(
    #         user=other_user,
    #         meal_question=self.meal_question1,
    #         answer_type='choice',
    #         answer_choice='a lot'
    #     )

    #     url = meal_user_url(self.meal_question1.id)
    #     res = self.client.get(url)

    #     meal_by_user = MealUser.objects.all().filter(user=self.user)
    #     serializer = MealUserSerializer(meal_by_user, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

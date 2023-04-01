"""
Test for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models"""

    # Test User Model
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new user"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@EXAMPLE.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_raise_error_when_email_is_blank(self):
        """Test raise error when email is blank"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test create superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # Test models about Meal
    def test_create_meal_question(self):
        """Test creating a MealQuestion is successful"""
        meal_question = models.MealQuestion.objects.create(
            question='How many processed food did you ate yesterday'
        )

        self.assertEqual(str(meal_question), meal_question.question)

    def test_create_vegetable(self):
        """Test creating vegetable is successful"""
        vegetable = models.MealVegetable.objects.create(
            vegetable='トマト',
            color='赤',
            varieties='果菜類'
        )

        self.assertEqual(str(vegetable), vegetable.vegetable)

    def test_create_meal_user(self):
        """Test creating MealUser is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'tesTpass123'
        )
        meal_question = models.MealQuestion.objects.create(
            question='How many processed food did you ate yesterday'
        )
        meal = models.MealUser.objects.create(
            user=user,
            meal_question=meal_question,
            answer_type='choice',
            answer_choice='none'
        )

        self.assertEqual(str(meal), meal.answer_choice)

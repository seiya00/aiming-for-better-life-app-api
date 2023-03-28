"""
Test for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': 'male',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_already_exists_error(self):
        """Test an error is returned if email already exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': 'female'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test an error is returned if password is less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'te',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': 'other'
        }
        # create_user(**payload) this isn't good
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_not_included_uppercase(self):
        """Test an error is returned if password doesn't include uppercase letter"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': 'male'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_not_included_number(self):
        """Test an error is returned if password doesn't include uppercase letter"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': 'male'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_user_with_gender_is_required_error(self):
        """Test an error is returned if gender is blank"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': 'Taro',
            'last_name': 'Test',
            'gender': '',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_user_with_lastname_is_required_error(self):
        """Test an error is returned if last_name is blank"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': 'Taro',
            'last_name': '',
            'gender': 'male'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_first_name_required_error(self):
        """Test an error is returned if first_name is blank"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': '',
            'last_name': 'Test',
            'gender': 'male'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_gender_include_invalid_value_error(self):
        """Test an error is returned if first_name is blank"""
        payload = {
            'email': 'test@example.com',
            'password': 'tesTpass123',
            'first_name': '',
            'last_name': 'Test',
            'gender': '男性'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""

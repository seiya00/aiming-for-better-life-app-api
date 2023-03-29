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
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()

    # Test for create user API

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
        """Test error returned if password doesn't include uppercase"""
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
        """Test error returned if password doesn't include number"""
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

    # Test create token for user API

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {
            'first_name': 'Test',
            'last_name': 'Taro',
            'gender': 'male',
            'email': 'test@example.com',
            'password': 'tesTpass123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_email(self):
        """Test posting a blank email returns an error"""
        payload = {'email': '', 'password': 'tesTpass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='tesTpas123',
            first_name='Taro',
            last_name='Test',
            gender='male'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'gender': self.user.gender
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the autheticated user"""
        payload = {'first_name': 'Updated', 'password': 'Newpass123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

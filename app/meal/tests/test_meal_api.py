"""
Tests for meal APIs
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Meal

from meal.serializers import MealSerializer


def create_meal(user, **params):
    """Create and return a sample meal object"""
    defaults = {
        ''
    }
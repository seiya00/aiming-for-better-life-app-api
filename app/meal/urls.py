"""
URL mappings for the meal app
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from meal import views


router = DefaultRouter()
router.register('meal-question', views.MealQuestionViewSet)
router.register('meal-user', views.MealUserViewSet)

app_name = 'meal'

urlpatterns = [
    path('', include(router.urls))
]

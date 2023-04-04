"""
URL mappings for the meal app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from meal import views


router = DefaultRouter()
router.register('questions', views.MealQuestionViewSet)
router.register('me', views.MealUserViewSet)

app_name = 'meal'

urlpatterns = [
    path('', include(router.urls)),
    # path('questions/', views.MealQuestionViewSet, name='meal-list'),
    # path('me/', views.MealUserViewSet, name='meal-user')
]

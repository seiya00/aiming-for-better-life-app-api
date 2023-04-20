"""
URL mappings for sleep app
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from sleep import views


router = DefaultRouter()
router.register('questions', views.SleepQuestionViewSet)
router.register('me', views.SleepUserViewSet)

app_name = 'sleep'

urlpatterns = [
    path('', include(router.urls)),
]
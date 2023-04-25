"""
URL mapping for the question app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from question import views


router = DefaultRouter()
router.register('questions', views.QuestionsViewSet)

app_name = 'question'

urlpatterns = [
    path('', include(router.urls)),
]

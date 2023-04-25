"""
URL mappings for the answer app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from answer import views


router = DefaultRouter()
router.register('answer', views.AnswerViewSet)

app_name = 'answer'

urlpatterns = [
    path('', include(router.urls)),
]
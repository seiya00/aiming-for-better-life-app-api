"""
Views for sleep APIs
"""
from rest_framework import viewsets
from rest_framework.authetication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

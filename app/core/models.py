"""
Database model
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    GENDER_CHOICES = [
        ('male', '男性'),
        ('female', '女性'),
        ('other', '回答なし')
    ]
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # birth_date = models.DateField(null=False)
    # user_name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class Home(models.Model):
#     """Home object"""
#     pass


class MealQuestion(models.Model): # Meal
    """Meal questions object"""
    question = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class MealVegetable(models.Model):
    """Vegetable object"""
    vegetable = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=255)
    varieties = models.CharField(max_length=255)

    def __str__(self):
        return self.vegetable


class MealUser(models.Model):
    """Meal object"""
    HOW_MANY_CHOICES = [
        ('none', '無し'),
        ('a bit', '少し'),
        ('normal', '普通'),
        ('a lot', 'たくさん')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    meal_question = models.ForeignKey(
        MealQuestion,
        on_delete=models.CASCADE,
        null=True
    )
    vegetable_question = models.ForeignKey(
        MealVegetable,
        on_delete=models.CASCADE,
        null=True
    )
    is_allergy = models.BooleanField(default=False)
    is_unnecessary = models.BooleanField(default=False)
    answer_type = models.CharField(max_length=255) # フロントエンドで回答を送る時に裏で回答の種類を送信
    answer_choice = models.CharField(max_length=10, choices=HOW_MANY_CHOICES, null=True)
    answer_int = models.IntegerField(null=True)
    answer_bool = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_choice


# class Sleep(models.Model):
#     """Sleep object"""
#     pass


# class SleepQuestion(models.Model):
#     """Sleep questions object"""
#     pass

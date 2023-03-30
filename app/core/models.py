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
        ('other', 'その他')
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


class Meal(models.Model):
    """Meal object"""
    HOW_MANY_CHOICES = [
        ('none', '無し'),
        ('a bit', '少し'),
        ('normal', '普通'),
        ('a lot', 'たくさん')
    ]
    user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    processed_food = models.CharField(max_length=10,
                                      choices=HOW_MANY_CHOICES)
    fried_food = models.CharField(max_length=10, choices=HOW_MANY_CHOICES)
    could_control_appetite = models.BooleanField(default=False)

    def __str__(self):
        return self.processed_food




# class MealQuestion(models.Model):
#     """Meal questions object"""
#     pass


# class Vegetable(models.Model):
#     """Vegetable object"""
#     pass


# class VegetableQuestion(models.Model):
#     """Vegetable questions object"""


# class Sleep(models.Model):
#     """Sleep object"""
#     pass


# class SleepQuestion(models.Model):
#     """Sleep questions object"""
#     pass

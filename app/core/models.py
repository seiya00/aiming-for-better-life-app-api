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
        ('男性', '男性'),
        ('女性', '女性')
    ]
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    # birth_date = models.DateField(null=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class Home(models.Model):
#     """Home object"""
#     pass


class Questions(models.Model):
    """Questions object"""
    question = models.CharField(max_length=50)
    question_type = models.CharField(max_length=10)
    answer_type = models.CharField(max_length=10)
    answer1 = models.CharField(max_length=10, null=True)
    answer2 = models.CharField(max_length=10, null=True)
    answer3 = models.CharField(max_length=10, null=True)
    answer4 = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.question


class Vegetable(models.Model):
    """Vegetable object"""
    vegetable = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=255)
    varieties = models.CharField(max_length=255)

    def __str__(self):
        return self.vegetable


class Answer(models.Model):
    """Answer object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        null=True
    )
    vegetable = models.ForeignKey(
        Vegetable,
        on_delete=models.CASCADE,
        null=True
    )
    is_allergy = models.BooleanField(default=False)
    is_unnecessary = models.BooleanField(default=False)
    answer_type = models.CharField(max_length=255)
    answer_choice = models.CharField(max_length=10, null=True)
    answer_int = models.IntegerField(null=True)
    answer_bool = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_type

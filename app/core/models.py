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
from django.core.exceptions import ValidationError


ANSWER_CHOICES = [
    ('選択式', '選択'),
    ('真偽値', '真偽'),
    ('数字', '数字')
]
QUESTION_CHOICES = [
    ('食事', '食事'),
    ('運動', '運動'),
    ('睡眠', '睡眠')
]
ANSWER1_CHOICE_CHOICES = [
    ('ゼロ', 'ゼロ'),
    ('だるい', 'だるい'),
]
ANSWER2_CHOICE_CHOICES = [
    ('少し', '少し'),
    ('少しだるい', '少しだるい'),
    ('１〜２回', '１〜２回'),
]
ANSWER3_CHOICE_CHOICES = [
    ('まあまあ', 'まあまあ'),
    ('普通', '普通'),
    ('３回以上', '３回以上'),
]
ANSWER4_CHOICE_CHOICES = [
    ('たくさん', 'たくさん'),
    ('良い', '良い'),
]

ANSWER1_BOOL_CHOICES = [
    (True, 'はい'),
]

ANSWER2_BOOL_CHOICES = [
    (False, 'いいえ'),
]

# def validate_contains_for_answer1(value):
#     """Check validation of answer1 field"""
#     if "ゼロ" or True not in value:
#         raise ValidationError("The value must contain 'ゼロ' or True")

# def validate_contains_for_answer1(value):
#     """Check validation of answer1 field"""
#     if "少し" or False not in value:
#         raise ValidationError("The value must contain '少し' or False")

# def validate_contains_for_answer1(value):
#     """Check validation of answer1 field"""
#     if "まあまあ" not in value:
#         raise ValidationError('The value must contain \'まあまあ\'')

# def validate_contains_for_answer1(value):
#     """Check validation of answer1 field"""
#     if "たくさん" not in value:
#         raise ValidationError("The value must contain 'たくさん'")


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
    question_type = models.CharField(max_length=10, choices=QUESTION_CHOICES)
    answer_type = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    is_neccessary = models.BooleanField(default=True)
    answer1_choice = models.CharField(max_length=10, blank=True, choices=ANSWER1_CHOICE_CHOICES)
    answer2_choice = models.CharField(max_length=10, blank=True, choices=ANSWER2_CHOICE_CHOICES)
    answer3_choice = models.CharField(max_length=10, blank=True, choices=ANSWER3_CHOICE_CHOICES)
    answer4_choice = models.CharField(max_length=10, blank=True, choices=ANSWER4_CHOICE_CHOICES)
    answer1_bool = models.BooleanField(null=True, blank=True, choices=ANSWER1_BOOL_CHOICES)
    answer2_bool = models.BooleanField(null=True, blank=True, choices=ANSWER2_BOOL_CHOICES)


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
    answer_type = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    answer_choice = models.CharField(max_length=10, null=True)
    answer_int = models.IntegerField(null=True)
    answer_bool = models.BooleanField(null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.answer_type

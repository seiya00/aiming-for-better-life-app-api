"""
Django admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'first_name', 'gender']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'gender')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_family',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'gender',
                'is_active',
                'is_staff',
                'is_family',
                'is_superuser'
            )
        }),
    )


class QuestionsAdmin(admin.ModelAdmin):
    """Define the admin pages for questions model"""
    ordering = ['id']
    list_display = ['question', 'question_type', 'answer_type', 'answer1', 'answer2', 'answer3', 'answer4']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Questions)
admin.site.register(models.Vegetable)
admin.site.register(models.Answer)

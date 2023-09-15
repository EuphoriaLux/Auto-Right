from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',
        'has_completed_step1', 'has_completed_step2', 'has_completed_step3'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser',
        'has_completed_step1', 'has_completed_step2', 'has_completed_step3'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Onboarding Status', {'fields': ('has_completed_step1', 'has_completed_step2', 'has_completed_step3')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

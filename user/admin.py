from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    list_display = ('national_id', 'mobile', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('national_id', 'mobile')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('national_id', 'mobile', 'first_name', 'last_name')}),
    )

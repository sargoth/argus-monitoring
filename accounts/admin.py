from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomAdminUserChangeForm, CustomAdminUserCreationForm

UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    form = CustomAdminUserChangeForm
    add_form = CustomAdminUserCreationForm

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ["display_name", "timezone"]
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ["email", "display_name", "timezone"]
        }),
    )
    list_display = UserAdmin.list_display + ("display_name", "timezone")

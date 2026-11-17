from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ["display_name", "timezone"]
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ["display_name", "timezone"]
        }),
    )
    list_display = UserAdmin.list_display + ("display_name", "timezone")

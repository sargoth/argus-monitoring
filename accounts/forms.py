from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm, UserChangeForm

from accounts.mixins import CleanEmailMixin

UserModel = get_user_model()


class UserRegistrationForm(CleanEmailMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("email", "timezone")


class CustomAdminUserCreationForm(CleanEmailMixin, AdminUserCreationForm):
    pass


class CustomAdminUserChangeForm(CleanEmailMixin, UserChangeForm):
    pass

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm, UserChangeForm
from django.forms import ModelForm, EmailField

from accounts.mixins import CleanEmailMixin

UserModel = get_user_model()


class UserRegistrationForm(CleanEmailMixin, UserCreationForm):
    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = UserCreationForm.Meta.fields + ("email", "timezone")


class CustomAdminUserCreationForm(CleanEmailMixin, AdminUserCreationForm):
    pass


class CustomAdminUserChangeForm(CleanEmailMixin, UserChangeForm):
    pass


class UserProfileUpdateForm(CleanEmailMixin, ModelForm):
    class Meta:
        model = UserModel
        fields = ["email", "display_name", "timezone"]

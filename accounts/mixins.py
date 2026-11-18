from django import forms
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CleanEmailMixin:
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if UserModel.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

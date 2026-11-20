from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from accounts.choices import fetch_timezone_choices


class User(AbstractUser):
    display_name = models.CharField(
        max_length=150,
        blank=True
    )
    timezone = models.CharField(
        max_length=50,
        choices=fetch_timezone_choices,
        default='UTC'
    )
    email = models.EmailField(
        blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_user_email',
                violation_error_message="This email address is already in use."
            )
        ]

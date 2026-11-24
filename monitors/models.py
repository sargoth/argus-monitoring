from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, URLValidator
from django.db import models
from django.db.models.functions import Lower


class Monitor(models.Model):
    class Status(models.TextChoices):
        UP = "up", "Up"
        DOWN = "down", "Down"
        PENDING = "pending", "Pending"

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="monitors"
    )
    name = models.CharField(
        max_length=150,
        help_text="Service name"
    )
    url = models.URLField(
        validators=[URLValidator(schemes=["http", "https"])],
        help_text="URL or API endpoint that will be checked."
    )
    status = models.CharField(
        max_length=10,
        help_text="Status of the monitored service.",
        choices=Status.choices,
        default=Status.PENDING
    )
    is_enabled = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the service was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the service was last updated."
    )
    tags = models.ManyToManyField(
        to="Tag",
        related_name="monitors",
        blank=True,
        help_text="Tags that can help organize the monitors."
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tags"
    )
    name = models.CharField(
        max_length=150,
        help_text="Name of the tag"
    )
    color = models.CharField(
        max_length=7,
        default="#64748B",
        validators=[
            RegexValidator(
                regex=r'^#[0-9A-Fa-f]{6}$'
            )
        ],
        help_text="Choose a color for this tag. Default is gray."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when tag was created."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                models.F("owner"),
                name="unique_tag_name_per_user"
            )
        ]

    def __str__(self) -> str:
        return self.name


class MonitorCheck(models.Model):
    monitor = models.ForeignKey(
        to=Monitor,
        on_delete=models.CASCADE,
        related_name="checks"
    )
    checked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this check was done."
    )
    is_successful = models.BooleanField(
        default=False,
        help_text="Whether the check was successful."
    )
    response_time_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Response time in milliseconds."
    )
    http_status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(100),
            MaxValueValidator(599)
        ],
        help_text="HTTP status code returned by the check."
    )
    error_message = models.TextField(
        blank=True,
        help_text="Error details in case the check failed."
    )

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self) -> str:
        return (
            f"{self.monitor.name} - {'Successful' if self.is_successful else 'Failed'} "
            f"{self.http_status_code or 'N/A'} at {self.checked_at}"
        )

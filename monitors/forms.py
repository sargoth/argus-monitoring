from django import forms
from django.core.exceptions import ValidationError

from monitors.models import Tag, Monitor


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
        widgets = {
            "color": forms.ColorInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"]
        tags_queryset = Tag.objects.filter(owner=self.user, name__iexact=name).exclude(pk=self.instance.pk)

        if tags_queryset.exists():
            raise ValidationError("A tag with this name already exists.")

        return name


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ["name", "url", "is_enabled", "tags"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.filter(owner=user)

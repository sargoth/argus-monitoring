from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from monitors.forms import TagForm
from monitors.models import Tag


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "monitors/tag_create.html"
    success_url = reverse_lazy("monitors:list_tags")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "monitors/tag_list.html"
    context_object_name = "tags"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user).order_by(Lower("name"))


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "monitors/tag_update.html"
    success_url = reverse_lazy("monitors:list_tags")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "monitors/tag_delete.html"
    success_url = reverse_lazy("monitors:list_tags")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

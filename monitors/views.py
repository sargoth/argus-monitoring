from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from monitors.forms import TagForm, MonitorForm
from monitors.models import Tag, Monitor


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


class MonitorListView(LoginRequiredMixin, ListView):
    model = Monitor
    template_name = "monitors/monitor_list.html"
    context_object_name = "monitors"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return (queryset.filter(owner=self.request.user).
                prefetch_related("tags").order_by(Lower("name")))


class MonitorCreateView(LoginRequiredMixin, CreateView):
    model = Monitor
    form_class = MonitorForm
    template_name = "monitors/monitor_create.html"
    success_url = reverse_lazy("monitors:list_monitors")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MonitorDetailView(LoginRequiredMixin, DetailView):
    model = Monitor
    template_name = "monitors/monitor_detail.html"
    context_object_name = "monitor"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user).prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_checks"] = self.object.checks.all()[:10]
        return context


class MonitorUpdateView(LoginRequiredMixin, UpdateView):
    model = Monitor
    form_class = MonitorForm
    template_name = "monitors/monitor_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user

        return kwargs

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get_success_url(self):
        final_url = reverse("monitors:detail_monitor", kwargs={"pk": self.object.pk})
        return final_url


class MonitorDeleteView(LoginRequiredMixin, DeleteView):
    model = Monitor
    template_name = "monitors/monitor_delete.html"
    success_url = reverse_lazy("monitors:list_monitors")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

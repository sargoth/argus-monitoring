from django.contrib import admin

from monitors.models import Monitor, Tag, MonitorCheck


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "url", "status", "is_enabled", "created_at"]
    list_filter = ["status", "is_enabled", "created_at"]
    search_fields = ["name", "url", "owner__username"]
    readonly_fields = ["status", "created_at", "updated_at"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "color", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "owner__username"]
    readonly_fields = ["created_at"]


@admin.register(MonitorCheck)
class MonitorCheckAdmin(admin.ModelAdmin):
    list_display = ["monitor", "checked_at", "is_successful", "response_time_ms", "http_status_code"]
    list_filter = ["checked_at", "is_successful"]
    search_fields = ["monitor__name", "monitor__url"]
    list_select_related = ["monitor"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Website


@admin.register(Website)
class WebsiteAdmin(ModelAdmin):
    list_display = ["user", "file", "title", "_url", "_theme", "template_type", "created_at"]
    search_fields = ["title", "user__username", "user__email", "url"]
    list_filter = ["theme__theme", "theme__template_type", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "theme")
    
    @admin.display(description="Theme")
    def _theme(self, obj):
        return obj.theme.theme if obj.theme else "No Theme"
    
    @admin.display(description="Template Type")
    def template_type(self, obj):
        return obj.theme.template_type if obj.theme else "No Template Type"
    
    @admin.display(description="URL")
    def _url(self, obj):
        return obj.get_absolute_url()

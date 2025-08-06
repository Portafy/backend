from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Website, WebsiteContent, ThemeConfig


@admin.register(Website)
class WebsiteAdmin(ModelAdmin):
    list_display = [
        "user",
        "file",
        "title",
        "slug",
        "_theme",
        "template_type",
        "created_at",
    ]
    search_fields = ["title", "user__username", "user__email", "slug"]
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
    def url(self, obj):
        return obj.get_absolute_url()


# Improved WebsiteContent admin
@admin.register(WebsiteContent)
class WebsiteContentAdmin(ModelAdmin):
    list_display = ["user", "content_preview", "created_at"]
    search_fields = ["user__username", "user__email"]
    ordering = ["-created_at"]

    @admin.display(description="Content Preview")
    def content_preview(self, obj):
        # Show a short preview of the content (first 50 chars)
        content = obj.content
        if not content:
            return "No Content"
        return str(content)[:50] + ("..." if content and len(str(content)) > 50 else "")


# Improved ThemeConfig admin
@admin.register(ThemeConfig)
class ThemeConfigAdmin(ModelAdmin):
    list_display = [
        "user",
        "name",
        "theme_display",
        "template_type_display",
        "config_preview",
        "created_at",
    ]
    search_fields = ["user__username", "user__email", "name"]
    ordering = ["-created_at"]

    @admin.display(description="Theme")
    def theme_display(self, obj):
        return obj.theme

    @admin.display(description="Template Type")
    def template_type_display(self, obj):
        return obj.template_type

    @admin.display(description="Config Preview")
    def config_preview(self, obj):
        config = obj.config

        if not config:
            return "No Config"
        return str(config)[:50] + ("..." if config and len(str(config)) > 50 else "")

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Website, Video

# Register your models here.
@admin.register(Website)
class WebsiteAdmin(ModelAdmin):
    list_display = ["user", "title", "slug", "theme", "type", "created_at"]
    search_fields = ["title", "user__username", "user__email", "slug"]
    list_filter = ["theme", "type", "created_at"]
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return True


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ["title", "user", "website", "web_link", "uploaded_at"]
    search_fields = [
        "title",
        "website__title",
        "website__slug",
        "website__user__username",
        "website__user__email",
    ]
    list_filter = ["uploaded_at"]
    ordering = ["-uploaded_at"]

    def has_add_permission(self, request):
        return False
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('website', 'website__user')
        return queryset


    @admin.display(description='User')
    def user(self, obj):
        return obj.website.user

    @admin.display(description='Website Link')
    def web_link(self, obj):
        return obj.website.slug
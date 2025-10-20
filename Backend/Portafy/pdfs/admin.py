from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(ModelAdmin):
    list_display = [
        "filename",
        "user_email",
        "uploaded_at",
    ]

    search_fields = [
        "filename",
        "user__email",
    ]
    list_filter = ["uploaded_at"]
    ordering = ["-uploaded_at"]

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")

    @admin.display(description="Email")
    def user_email(self, obj):
        return obj.user.email
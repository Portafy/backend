from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(ModelAdmin):
    list_display = [
        "website",
        "user_username",
        "user_email",
        "filename",
        "uploaded_at",
    ]
    
    search_fields = [
        "website__title",
        "file",
        "user__username",
        "user__email",
    ]
    list_filter = ["uploaded_at"]
    ordering = ["-uploaded_at"]
    
    def has_add_permission(self, request):
        return False
    
    @admin.display(description='File Name')
    def filename(self, obj):
        return obj.file.split("/")[-1]
    
    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email
    
    @admin.display(description='Username')
    def user_username(self, obj):
        return obj.user.username


from django.contrib import admin
from django.contrib.admin import ModelAdmin

from django.db.models import Count

from .models import User, Customer


# Register your models here.
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
    ]
    search_fields = ["email", "username", "first_name", "last_name"]
    list_filter = []
    ordering = ["first_name", "last_name", "username"]
    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "phone"]}),
        ("Permissions", {"fields": ["is_staff", "is_active"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],  # css style for a wider form layout
                "fields": [
                    "email",
                    "username",
                    "password1",
                    "password2",
                ],  # password1 and password2 for confirming the passwords when creating a new user
            },
        ),
    ]


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ["user", "subscription"]
    list_filter = ["subscription"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("user")
        queryset = queryset.annotate(_website_count=Count("user__websites"))
        return queryset

    @admin.display(description="Website Count")
    def website_count(self, obj):
        return getattr(obj, "_website_count", 0)

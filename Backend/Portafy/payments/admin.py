from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Payment
# Register your models here.

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ["user", "website", "amount", "payment_gateway", "reference_id", "paid_at"]
    search_fields = ["user__username", "user__email", "amount", "is_successful", "reference_id"]
    list_filter = ["is_successful", "created_at", "payment_gateway"]
    ordering = ["-updated_at", "-created_at"]

    @admin.display(description="Paid At")
    def paid_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    def has_add_permission(self, request):
        return False

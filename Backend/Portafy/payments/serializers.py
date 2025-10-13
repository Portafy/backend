from decimal import Decimal
from typing import Optional

from rest_framework import serializers

from websites.models import Website


class InitiatePaymentSerializer(serializers.Serializer):
    website_id = serializers.IntegerField()
    email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10, default="ETB")
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    title = serializers.CharField(required=False, allow_blank=True, max_length=120)
    return_url = serializers.URLField(required=False)

    def validate_amount(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        website_id = attrs.get("website_id")

        try:
            website = Website.objects.get(id=website_id)
        except Website.DoesNotExist:
            raise serializers.ValidationError({"website_id": "Website not found."})

        # Ownership check (non-admin)
        if user and not getattr(user, "is_staff", False):
            owner_id = getattr(website, "user_id", None) or (getattr(website.user, "id", None) if hasattr(website, "user") else None)
            if owner_id != getattr(user, "id", None):
                raise serializers.ValidationError("You do not own this website.")

        attrs["website"] = website
        return attrs


class VerifyPaymentSerializer(serializers.Serializer):
    tx_ref = serializers.CharField(max_length=200)

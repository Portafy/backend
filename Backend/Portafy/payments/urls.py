from django.urls import path
from .views import (
    InitiatePaymentAPIView,
    ChapaWebhookAPIView,
    VerifyPaymentAPIView,
)

app_name = "payments"

urlpatterns = [
    # Auth required
    path("initiate/", InitiatePaymentAPIView.as_view(), name="initiate"),
    path("verify/", VerifyPaymentAPIView.as_view(), name="verify"),
    # Public webhook (no auth)
    path("webhook/chapa/", ChapaWebhookAPIView.as_view(), name="chapa_webhook"),
]

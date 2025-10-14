from uuid import uuid4
from typing import Any, Dict, cast
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import InitiatePaymentSerializer, VerifyPaymentSerializer
from .chapa import initialize as chapa_initialize, verify as chapa_verify


class InitiatePaymentAPIView(APIView):
    """
    Starts a Chapa payment and returns a checkout_url to redirect the user.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InitiatePaymentSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data: Dict[str, Any] = cast(Dict[str, Any], serializer.validated_data)

        website = data["website"]
        amount = data["amount"]
        email = data["email"]
        currency = str(data.get("currency", "ETB"))
        first_name = data.get("first_name") or None
        last_name = data.get("last_name") or None
        title = data.get("title") or "Website Source Code Purchase"
        return_url = data.get("return_url") or None

        tx_ref = f"web-{website.id}-{request.user.id}-{uuid4().hex[:12]}"

        # Create a pending payment record
        payment = Payment.objects.create(
            user=request.user,
            website=website,
            email=email,
            amount=amount,
            payment_gateway="chapa",
            reference_id=tx_ref,
            is_successful=False,
        )

        callback_url = request.build_absolute_uri(reverse("payments:chapa_webhook"))

        try:
            init_resp = chapa_initialize(
                tx_ref=tx_ref,
                amount=str(amount),
                currency=currency,
                email=email,
                first_name=first_name,
                last_name=last_name,
                callback_url=callback_url,
                return_url=return_url,
                title=title,
            )
            return Response(
                {"checkout_url": init_resp["checkout_url"], "tx_ref": tx_ref},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            # Rollback the pending payment if initialization fails
            payment.delete()
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChapaWebhookAPIView(APIView):
    """
    Receives server-to-server callback from Chapa.
    Verifies tx_ref and marks Payment as successful when verified.
    Public endpoint (no auth).
    """

    permission_classes = [AllowAny]
    authentication_classes = []  # Ensure no auth is required

    def post(self, request):
        tx_ref = request.data.get("tx_ref") or (request.data.get("data") or {}).get(
            "tx_ref"
        )
        if not tx_ref:
            return Response(
                {"detail": "Missing tx_ref"}, status=status.HTTP_400_BAD_REQUEST
            )

        verify_data = chapa_verify(tx_ref)
        success = bool(verify_data.get("success"))
        raw = verify_data.get("raw") or {}
        server_data = (raw.get("data") or {}) if isinstance(raw, dict) else {}
        server_tx_ref = server_data.get("tx_ref") or tx_ref
        server_amount = server_data.get("amount")
        server_currency = server_data.get("currency")

        try:
            payment = Payment.objects.get(reference_id=tx_ref)
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if success:
            # Basic reconciliation to prevent spoofing: ensure tx_ref matches and amount (if provided) equals local record
            if server_tx_ref and server_tx_ref != tx_ref:
                return Response({"success": False, "detail": "tx_ref mismatch"}, status=status.HTTP_400_BAD_REQUEST)
            if server_amount is not None:
                try:
                    if Decimal(str(server_amount)) != payment.amount:
                        return Response({"success": False, "detail": "amount mismatch"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    # If parsing fails, fall back to success based on provider status only
                    pass
            if not payment.is_successful:
                payment.is_successful = True
                payment.save(update_fields=["is_successful", "updated_at"])
            return Response({"success": True}, status=status.HTTP_200_OK)

        return Response({"success": False}, status=status.HTTP_200_OK)


class VerifyPaymentAPIView(APIView):
    """
    Client-side verification endpoint (optional).
    Frontend can call this with tx_ref to confirm completion.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tx_ref: str = cast(Dict[str, Any], serializer.validated_data)["tx_ref"]

        verify_data = chapa_verify(tx_ref)
        success = bool(verify_data.get("success"))
        raw = verify_data.get("raw") or {}
        server_data = (raw.get("data") or {}) if isinstance(raw, dict) else {}
        server_amount = server_data.get("amount")

        payment = (
            Payment.objects.filter(reference_id=tx_ref, user=request.user).first()
        )
        if success and payment:
            # Basic reconciliation on amount if provider returned it
            if server_amount is not None:
                try:
                    if Decimal(str(server_amount)) != payment.amount:
                        return Response(
                            {"success": False, "detail": "amount mismatch"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception:
                    pass
            if not payment.is_successful:
                payment.is_successful = True
                payment.save(update_fields=["is_successful", "updated_at"])

        return Response(
            {"success": success, "tx_ref": tx_ref, "found": bool(payment)},
            status=status.HTTP_200_OK,
        )

from weakref import ref
import requests, uuid, os
from django.conf import settings
from django.http import JsonResponse
from .models import Payment

def initiate_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    data = request.POST
    email = data.get("email")
    amount = data.get("amount")
    website = data.get("website")
    reference_id = str(uuid.uuid4())
    
    payment = Payment.objects.create(
        user=request.user,
        email=email,
        amount=amount,
        reference_id=reference_id
    )
    
    payload = {
        "email": email,
        "amount": amount,
        "currency": os.getenv("CURRENCY", "ETB"),
        "website": website,
        "reference_id": reference_id,
        "callback_url": "https://yourdomain.com/api/payments/verify/",
        "return_url": settings.FRONTEND_PAYMENT_SUCCESS_URL,
        "customization[title]": "Bella Portfolio Payment",
        "customization[description]": "Support or subscription payment",
    }
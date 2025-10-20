import requests
import uuid
import os
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
    
    headers = {
        "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.post("https://api.chapa.co/v1/transaction/intialize", json=payload, headers=headers)
    res_data = response.json()
    
    if response.status_code == 200:
        payment.checkout_url = res_data.get("data", {}).get("checkout_url")
        payment.save()
        return JsonResponse({"checkout_url": payment.checkout_url}, status=200)
    
    return JsonResponse({"error": "Failed to initiate payment"}, status=500)
        
        
def verify_payment(request):
    reference_id = request.GET.get("reference_id")
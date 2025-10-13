import requests
from typing import Optional, Dict, Any
from decouple import config


CHAPA_BASE_URL = config("CHAPA_BASE_URL", default="https://api.chapa.co")
CHAPA_SECRET_KEY = config("CHAPA_SECRET_KEY", default="")


def _headers() -> Dict[str, str]:
    """
    Build auth headers for Chapa API.
    """
    if not CHAPA_SECRET_KEY:
        raise RuntimeError("CHAPA_SECRET_KEY is not set in environment.")
    return {
        "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def initialize(
    tx_ref: str,
    amount: str,
    currency: str,
    email: str,
    *,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    callback_url: Optional[str] = None,
    return_url: Optional[str] = None,
    title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initialize a Chapa transaction.
    Args:
        tx_ref: Your unique transaction reference (store in DB).
        amount: Decimal/str amount (e.g. "500.00").
        currency: e.g. "ETB" or "USD".
        email: Payer email.
        first_name, last_name: Optional payer names.
        callback_url: Server-to-server webhook URL (Chapa will POST here).
        return_url: Frontend URL to redirect customer after payment.
        title: Optional payment title/description.
    Returns:
        { "checkout_url": str, "tx_ref": str, "raw": dict }
    Raises:
        RuntimeError on API error.
    """
    url = f"{CHAPA_BASE_URL}/v1/transaction/initialize"
    payload: Dict[str, Any] = {
        "amount": str(amount),
        "currency": currency,
        "email": email,
        "tx_ref": tx_ref,
    }
    if first_name:
        payload["first_name"] = first_name
    if last_name:
        payload["last_name"] = last_name
    if title:
        payload["title"] = title
    if callback_url:
        payload["callback_url"] = callback_url
    if return_url:
        payload["return_url"] = return_url

    resp = requests.post(url, json=payload, headers=_headers(), timeout=30)
    data = resp.json() if resp.content else {}

    # Chapa returns { "status": "success" | "error", "data": {...} }
    if resp.status_code >= 400 or not data.get("status") == "success":
        raise RuntimeError(f"Chapa initialize failed: {data}")

    checkout_url = (data.get("data") or {}).get("checkout_url")
    if not checkout_url:
        raise RuntimeError(f"Missing checkout_url in Chapa response: {data}")

    return {"checkout_url": checkout_url, "tx_ref": tx_ref, "raw": data}


def verify(tx_ref: str) -> Dict[str, Any]:
    """
    Verify a Chapa transaction by tx_ref.
    Returns:
        { "success": bool, "raw": dict }
    """
    url = f"{CHAPA_BASE_URL}/v1/transaction/verify/{tx_ref}"
    resp = requests.get(url, headers=_headers(), timeout=30)
    data = resp.json() if resp.content else {}

    # Example success schema: { "status": "success", "data": { "status": "success", ... } }
    success = data.get("status") == "success" and (data.get("data") or {}).get("status") == "success"
    return {"success": bool(success), "raw": data}

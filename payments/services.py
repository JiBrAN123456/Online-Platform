import requests
from django.conf import settings


def get_paypal_access_token():
    response = requests.post(
        f"{settings.PAYPAL_API_BASE}/v1/oauth/token",
        auth= (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        headers={"Accept":"application/json"},
        data= {"grant_type":"client_credentails"}
    )
    response.raise_for_status()
    return response.json()["access_token"]



def create_paypal_order(amount, currency="USD"):
    access_token = get_paypal_access_token()
    

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    body = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                }
            }
        ],
        "application_context": {
            "return_url": "http://localhost:8000/payments/execute/",
            "cancel_url": "http://localhost:8000/payments/cancel/"
        }
    }

    response = requests.post(
        f'{settings.PAYPAL_API_BASE}/v2/checkout/orders',
        headers=headers,
        json=body
    )
    response.raise_for_status()
    return response.json()
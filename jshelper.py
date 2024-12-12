import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
payment_url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
access_token_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'

def get_access_token():

    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(access_token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def payment_data_helper(amount, payee_email):
    payment_data = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [
            {
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "payee": {
                    "email": payee_email
                },
                "description": "Payment to a friend"
            }
        ],
        "redirect_urls": {
            "return_url": "https://example.com/return",
            "cancel_url": "https://example.com/cancel"
        }
    }

    return payment_data

def create_payment(amount, payee_email):

    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = payment_data_helper(float(amount), payee_email)
    response = requests.post(payment_url, headers=headers, json=payload)
    response.raise_for_status()
    payment_response = response.json()
    return payment_response

def get_payment_status(payment_id):
    access_token = get_access_token()
    payment_status_url = payment_url+'/'+payment_id
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(payment_status_url, headers=headers)
    response.raise_for_status()
    return response.json()

def execute_payment(payer_id, payment_id):
    access_token = get_access_token()
    execute_payment_url = payment_url+'/'+payment_id+'/execute'
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "payer_id": payer_id
    }
    response = requests.post(execute_payment_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


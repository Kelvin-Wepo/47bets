import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from rest_framework.response import Response
from dotenv import load_dotenv
import os

load_dotenv()

def stk_push(phone_number, amount):
    #accessing the token
    mpesa_consumer_key = os.getenv("mpesa_consumer_key")
    mpesa_consumer_secret = os.getenv("mpesa_consumer_secret")
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(api_url,auth=HTTPBasicAuth(mpesa_consumer_key,mpesa_consumer_secret))
    access_token = response.json()['access_token']

    #Initiating STK Push
    business_short_code = '174379'  # This is the paybill or till number
    lipa_na_mpesa_online_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    phone_number = phone_number
    lipa_na_mpesa_online_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    amount = amount
    callback_url = 'https://88dnd53k-8000.euw.devtunnels.ms/api/v1/callback_url/<id>'

    # Generate password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(business_short_code.encode() + lipa_na_mpesa_online_passkey.encode() + timestamp.encode()).decode('utf-8')

    # Define the request payload
    payload = {
        'BusinessShortCode': business_short_code,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': business_short_code,
        'PhoneNumber': phone_number,
        'CallBackURL': callback_url,
        'AccountReference': '47 bets',
        'TransactionDesc': 'Payment for goods'
    }

    # Set the headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Send the request
    response = requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers)
    data = response.json()
    return data






import os

import requests

import ibm_boto3 
from ibm_botocore.client import Config

COS_API_KEY = os.getenv("COS_API_KEY")
COS_INSTANCE_CRN = os.getenv("COS_INSTANCE_CRN")
COS_ENDPOINT = os.getenv("COS_ENDPOINT")
BUCKET_NAME = os.getenv("IBM_BUCKET")
BEARER_FILE = "volumental_bearer.txt"

cos = ibm_boto3.client(
    service_name="s3",
    ibm_api_key_id=COS_API_KEY,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version='oauth'),
    endpoint_url=COS_ENDPOINT
)

def get_stored_bearer() -> str:
    try:
        response = cos.get_object(Bucket=BUCKET_NAME, Key=BEARER_FILE)
        return response["Body"].read().decode("utf-8")
    except cos.exceptions.NoSuchKey:
        print("IBM Cloud Object Storage - No Bearer Found", flush=True)
        return None

def bearer_is_valid(url: str, bearer: str) -> bool:
    URL = url
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    response = requests.get(URL, headers=headers)
    status = response.status_code
    print(f"Volumental - Stored Bearer is Valid Check: {status}", flush=True)
    return status == 200

def get_new_bearer(url: str) -> bool:
    URL = f"{url}v1/auth"
    CLIENT_ID = os.getenv("VOL_CLIENT_ID")
    CLIENT_SECRET = os.getenv("VOL_CLIENT_SECRET")
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(URL, json=payload, headers=headers)
    status = response.status_code
    print(f"Volumental - Get New Bearer: {status}", flush=True)
    if status == 200:
        data = response.json()
        new_bearer = data["access_token"]
        return new_bearer
    print(response.text, flush=True)
    raise Exception("AUTHENTICATION ERROR")

def save_new_bearer(bearer):
    print("IBM Cloud Object Storage - Saving New Bearer", flush=True)
    cos.put_object(Bucket=BUCKET_NAME, Key=BEARER_FILE, Body=bearer)

def get_valid_bearer(url: str):
    stored_bearer = get_stored_bearer()
    if stored_bearer and bearer_is_valid(url, stored_bearer):
        return stored_bearer
    new_bearer = get_new_bearer(url)
    save_new_bearer(new_bearer)
    return new_bearer
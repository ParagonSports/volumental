import logging
import requests

from dotenv import load_dotenv, dotenv_values, set_key

load_dotenv(".env")

def update_authentication(url: str) -> bool:
    URL = f"{url}v1/auth"
    config = dotenv_values(".env")
    CLIENT_ID = config.get("VOL_CLIENT_ID")
    CLIENT_SECRET = config.get("VOL_CLIENT_SECRET")
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(URL, json=payload, headers=headers)
    print("Auth Update:", response)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        new_bearer = data["access_token"]
        set_key(".env", "VOL_BEARER", new_bearer)
        load_dotenv(override=True)
        return True
    raise Exception("AUTHENTICATION ERROR")

def check_authentication(url: str) -> bool:
    URL = url
    config = dotenv_values(".env")
    BEARER = config.get("VOL_BEARER")
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {BEARER}"
    }
    print("BEARER TEST", BEARER)
    response = requests.get(URL, headers=headers)
    print("Auth Check:", response)
    print(response.text)
    return response.status_code == 200

def authenticate(url: str):# Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()
    logger.info("Starting the AUTHENTICATION process...")
    auth_is_valid = check_authentication(url)
    if not auth_is_valid:
        auth_is_valid = update_authentication(url)
    logger.info("AUTHENTICATION loaded successfully.")
    return auth_is_valid
import os

from dotenv import dotenv_values
import requests

def replace_inventory(url, payload: dict) -> None:
    URL = f"{url}v1beta/paragon_sports/inventory?override=true"
    config = dotenv_values(".env")
    BEARER = config.get("VOL_BEARER")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {BEARER}"
    }

    response = requests.put(URL, json=payload, headers=headers)
    print(response)
    print(response.text)
import os
import logging

from dotenv import dotenv_values
import requests

def replace_inventory(url, payload: dict) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()
    URL = f"{url}v1beta/paragon_sports/inventory?override=true"
    BEARER = os.getenv("VOL_BEARER")
    print("BEARER TEST", BEARER)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {BEARER}"
    }

    response = requests.put(URL, json=payload, headers=headers)
    print("Replace Inv:", response)
    print(response.text)
    if response.status_code != 204:
        logger.error(f"Replace Inventory API: [{response.status_code}]")
    else:
        logger.info(f"Replace Inventory API: [{response.status_code}]")
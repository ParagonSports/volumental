import requests

def replace_inventory(url: str, bearer: str, payload: dict) -> None:
    URL = f"{url}v1beta/paragon_sports/inventory?override=true"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    response = requests.put(URL, json=payload, headers=headers)
    status = response.status_code
    print(f"Volumental - Replace Inventory: {status}", flush=True)
    if status != 204:
        print(response.text, flush=True)
        raise Exception("VOLUMENTAL INVENTORY UPLOAD FAILED")
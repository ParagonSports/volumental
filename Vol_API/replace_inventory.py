import requests

def replace_inventory(url: str, bearer: str, payload: dict) -> None:
    URL = f"{url}v1beta/paragon_sports/inventory?override=true"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {bearer}"
    }
    response = requests.put(URL, json=payload, headers=headers)
    print("Volumental - Replace Inventory:", response.status_code)
    print(response.text)
    if response.status_code != 204:
        raise Exception("VOLUMENTAL INVENTORY UPLOAD FAILED")
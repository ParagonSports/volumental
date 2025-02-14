import os
import io
from ftplib import FTP

from Utilities.create_df import create_df
from Utilities.get_table_cols import columns_map
from Utilities.build_inv_payload import build_inv_payload
from Vol_API.handle_auth import get_valid_bearer
from Vol_API.replace_inventory import replace_inventory

FTP_HOST = "paragon.hostedftp.com"
FTP_USERNAME = os.getenv("FTP_USER")
FTP_PASSWORD = os.getenv("FTP_PASS")
PRODUCT_DATA_FILE_PATH = "/IBM Cloud/product_data_for_volumental.xlsx"
VOL_URL = "https://api.volumental.dev/"
if not FTP_USERNAME or not FTP_PASSWORD:
    print("FTP Credentials not found!")
else:
    print("FTP Credentials loaded successfully.") 

ftp = FTP(FTP_HOST)
ftp.login(FTP_USERNAME, FTP_PASSWORD)

data = io.BytesIO()
ftp.retrbinary(f"RETR {PRODUCT_DATA_FILE_PATH}", data.write)
data.seek(0)
ftp.quit()

product_data_df = create_df(data, columns_map["product_data"])
inventory_payload = build_inv_payload(product_data_df)
print(f"Inventory Payload Built - Size: {len(inventory_payload)}")

vol_bearer = get_valid_bearer(VOL_URL)
replace_inventory(VOL_URL, vol_bearer, inventory_payload)
print("~ Volumental Inventory Update Complete ~")
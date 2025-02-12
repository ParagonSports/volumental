import os
import io
import logging
import sys
from ftplib import FTP

from Utilities.create_df import create_df
from Utilities.get_table_cols import columns_map
from Utilities.build_inv_payload import build_inv_payload
from Vol_API.handle_auth import authenticate
from Vol_API.replace_inventory import replace_inventory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()
logger.info("This message should appear in IBM Cloud Code Engine logs.")
print("Print statement test - should also appear in logs")

FTP_HOST = "paragon.hostedftp.com"
FTP_USERNAME = os.getenv("FTP_USER")
FTP_PASSWORD = os.getenv("FTP_PASS")
PRODUCT_DATA_FILE_PATH = "/IBM Cloud/25.02.10 - Product Data - Div 09, 10.xlsx"
VOL_URL = "https://api.volumental.dev/"
if not FTP_USERNAME or not FTP_PASSWORD:
    logger.error("FTP Credentials not found!")
else:
    logger.info("FTP Credentials loaded successfully.") 

ftp = FTP(FTP_HOST)
ftp.login(FTP_USERNAME, FTP_PASSWORD)

data = io.BytesIO()
ftp.retrbinary(f"RETR {PRODUCT_DATA_FILE_PATH}", data.write)
data.seek(0)
ftp.quit()

product_data_df = create_df(data, columns_map["product_data"])
inventory_payload = build_inv_payload(product_data_df)
logger.info(f"Inventory Payload Size: {len(inventory_payload)}")

authenticate(VOL_URL)
replace_inventory(VOL_URL, inventory_payload)
import pandas as pd

from typing import List

def build_inv_payload(df: pd.DataFrame) -> List[dict]:
    inventory = []
    for idx, row in df.iterrows():
        if row["Prim Size"] == "":
            continue
        row_dict = {
            "on_hand": row["On Hand Units"],
            "pos_id": "1",
            "product_id": row["Paragon SKU"],
        }
        inventory.append(row_dict)
    return inventory
import io

import pandas as pd

from typing import List

def set_data_types(str_cols: List[str], float_cols: List[str], int_cols: List[str]) -> dict:
    col_dtypes = {}
    for col in str_cols:
        col_dtypes[col] = str
    for col in float_cols:
        col_dtypes[col] = float
    for col in int_cols:
        col_dtypes[col] = int
    return col_dtypes

def set_na_vals(str_cols: List[str], float_cols: List[str], int_cols: List[str]) -> dict:
    na_vals = {}
    for col in str_cols:
        na_vals[col] = ""
    for col in float_cols:
        na_vals[col] = 0
    for col in int_cols:
        na_vals[col] = 0
    return na_vals

def create_df(file: io.BytesIO, cols: dict) -> pd.DataFrame:
    str_cols = cols["string"]
    float_cols = cols["float"]
    int_cols = cols["int"]
    all_cols = str_cols + float_cols + int_cols
    col_dtypes = set_data_types(str_cols, float_cols, int_cols)
    na_vals = set_na_vals(str_cols, float_cols, int_cols)
    df = pd.read_csv(file, usecols=all_cols, dtype=col_dtypes)
    df.fillna(value=na_vals, inplace=True)
    return df
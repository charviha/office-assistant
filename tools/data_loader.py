"""
data_loader.py
---------------
Loads all sample CSVs into pandas DataFrames once and caches them.
Every tool function in this package pulls data from here instead of
re-reading CSVs on every call.

If this project moves from CSVs to a real database later, this is the
ONLY file that needs to change — every function in the other modules
can stay exactly the same as long as the returned DataFrames keep the
same column names.
"""

import os
import pandas as pd

# Folder containing the CSV files. Override with the OFFICE_DATA_DIR
# environment variable if you place the data elsewhere (e.g. in Person 4's
# app deployment).
DATA_DIR = os.environ.get(
    "OFFICE_DATA_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"),
)

_cache = {}


def _load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV from DATA_DIR into a DataFrame, caching the result."""
    if filename not in _cache:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Expected data file not found: {path}. "
                f"Set the OFFICE_DATA_DIR environment variable if your CSVs live elsewhere."
            )
        df = pd.read_csv(path, dtype=str)  # read everything as string first, cast per-column below
        _cache[filename] = df
    return _cache[filename].copy()


def get_employees_df() -> pd.DataFrame:
    df = _load_csv("employees.csv")
    return df


def get_leave_balance_df() -> pd.DataFrame:
    df = _load_csv("leave_balance.csv")
    numeric_cols = [c for c in df.columns if c not in ("employee_id",)]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def get_expense_records_df() -> pd.DataFrame:
    df = _load_csv("expense_records.csv")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df


def get_office_locations_df() -> pd.DataFrame:
    return _load_csv("office_locations.csv")


def get_it_assets_df() -> pd.DataFrame:
    return _load_csv("IT_assets.csv")


def reload_all():
    """Clear the cache so the next call re-reads CSVs from disk.
    Useful after apply_leave()/submit_expense() write new rows, or in tests."""
    _cache.clear()

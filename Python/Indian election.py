"""
data.py
-------
Cleans the Indian National Level Election dataset (1977-2014).

Input : indian-national-level-election.csv (raw)
Output: clean_election_data.csv / clean_election_data.txt

Run:
    python data.py
"""

import pandas as pd
import numpy as np

RAW_FILE = "indian-national-level-election.csv"
OUT_CSV = "clean_election_data.csv"
OUT_TXT = "clean_election_data.txt"


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from all text (object/string) columns."""
    text_cols = [
        c for c in df.columns
        if df[c].dtype == object or str(df[c].dtype).lower() == "string"
    ]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()
    return df


def standardize_state_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge duplicate / inconsistent spellings of the same state into
    one canonical name.
    """
    state_map = {
        "Chattisgarh": "Chhattisgarh",
        "Orissa": "Odisha",
        "Pondicherry": "Puducherry",
        "Uttaranchal": "Uttarakhand",
        "Goa Daman & Diu": "Goa, Daman & Diu",
        "Nct Of Delhi": "National Capital Territory Of Delhi",
    }
    df["st_name"] = df["st_name"].replace(state_map)
    return df


def clean_pc_type(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize constituency-type codes and fill missing values."""
    df["pc_type"] = df["pc_type"].str.upper().str.strip()
    df["pc_type"] = df["pc_type"].fillna("UNKNOWN")
    return df


def clean_cand_sex(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize candidate sex codes and fill missing values."""
    df["cand_sex"] = df["cand_sex"].str.upper().str.strip()
    df["cand_sex"] = df["cand_sex"].fillna("UNKNOWN")
    return df


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Title-case candidate and constituency names for consistency."""
    df["cand_name"] = df["cand_name"].str.title()
    df["pc_name"] = df["pc_name"].str.title()
    return df


def enforce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure numeric columns have the correct dtype."""
    df["year"] = df["year"].astype(int)
    df["pc_no"] = df["pc_no"].astype(int)
    df["totvotpoll"] = df["totvotpoll"].astype(int)
    df["electors"] = df["electors"].astype(int)
    return df


def remove_bad_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicates and logically invalid rows."""
    before = len(df)
    df = df.drop_duplicates()
    df = df[df["totvotpoll"] >= 0]
    df = df[df["electors"] > 0]
    df = df[df["totvotpoll"] <= df["electors"]]
    after = len(df)
    print(f"Removed {before - after} duplicate/invalid rows.")
    return df.reset_index(drop=True)


def add_vote_share(df: pd.DataFrame) -> pd.DataFrame:
    """Add a helper column: vote share (%) of each candidate in their constituency."""
    df["vote_share_pct"] = (df["totvotpoll"] / df["electors"] * 100).round(2)
    return df


def clean_election_data(path: str) -> pd.DataFrame:
    df = load_data(path)
    df = clean_text_columns(df)
    df = standardize_state_names(df)
    df = clean_pc_type(df)
    df = clean_cand_sex(df)
    df = clean_names(df)
    df = enforce_types(df)
    df = remove_bad_rows(df)
    df = add_vote_share(df)

    # Final column order
    cols = [
        "st_name", "year", "pc_no", "pc_name", "pc_type",
        "cand_name", "cand_sex", "partyname", "partyabbre",
        "totvotpoll", "electors", "vote_share_pct",
    ]
    df = df[cols]
    return df


def save_outputs(df: pd.DataFrame):
    df.to_csv(OUT_CSV, index=False)
    df.to_csv(OUT_TXT, index=False, sep="\t")
    print(f"Saved cleaned data to '{OUT_CSV}' and '{OUT_TXT}'")


if __name__ == "__main__":
    cleaned_df = clean_election_data(RAW_FILE)
    print(cleaned_df.info())
    print(cleaned_df.head())
    save_outputs(cleaned_df)

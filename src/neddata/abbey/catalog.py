"""Loads datasets"""

# %%
from pathlib import Path

import pandas as pd

# --- Local Imports
from neddata import datamodel as dm
import neddata._utils as u

# --- Imports for testing
if __name__ == "__main__":
    from IPython.display import display

# %%
# =====================================================================
# === Init Catalogue
# =====================================================================


# ---------------------------------------------------------------------
# --- Manual Configuration

# => Configure the Dataset
DATASET = "neddata.abbey"  # < <project>.<package> = <database>.<dataset>
DB_URL = "https://raw.githubusercontent.com/HisQu/neddata/refs/heads/main/src"


# > Glob-Patterns of directories that become a DataDir 
# > Containing files will be downloaded as a whole (not catalogued as Datafiles)
DATADIR_PATTERNS = [
    "*RAGI*",  # < RAG Index
]

# %%
# => Make / update the pooch_registry.txt
# !! Repeat after every change
if __name__ == "__main__":
    dm.write_pooch_registry(dataset=DATASET)
    # %%


# %%
# ---------------------------------------------------------------------
# --- Make Catalogue
abbey_catalog: dm.Catalog = dm.make_catalog(
    dataset=DATASET,
    base_url=DB_URL,
    datadir_patterns=DATADIR_PATTERNS,
)

if __name__ == "__main__":
    print(abbey_catalog)  # > Print the catalogue object


# %%
# =====================================================================
# === Custom loading functions for specific files
# =====================================================================
# => Use globs/wildcards to register a function to multiple files at once!


@abbey_catalog.set_loader("Regests/2_ben-Cist Identifizierungen.csv")
def load_ben_cist_data(path: Path) -> pd.DataFrame:
    """Import CSV file that ignores the separator in the last column."""
    ### Read the whole file as plain text, one Python string per line
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    ### Split each line at the first 6 semicolons only
    rows = [line.split(";", 6) for line in lines]
    columns = rows[0]  # < first line is the header
    rows = rows[1:]  # < remove header from data
    ### Build the DataFrame and name your columns
    df = pd.DataFrame(rows, columns=columns).drop_duplicates()
    return df


if __name__ == "__main__":
    _key = "Regests/2_Ben-cist_Identifizierungen.csv"
    #  %%
    ### Load conventionally
    p = abbey_catalog[_key].path
    print(p)
    df = load_ben_cist_data(p)
    display(df)
    # %%
    ### Load from the catalogue
    print(abbey_catalog[_key].path)
    print(abbey_catalog[_key].loader)  # type: ignore
    df = abbey_catalog.load(_key)
    display(df)


# %%
@abbey_catalog.set_loader("KDB/KDB*.csv")
def load_utf8_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file with UTF-8 encoding."""
    df = pd.read_csv(path, encoding="utf-8", sep=";")
    ### Convert Lon and Lat to numeric if they exist
    if all(col in df.columns for col in ["Lon", "Lat"]):
        u.pd.lon_lat_to_numeric(df=df, columns=["Lon", "Lat"])
    return df


if __name__ == "__main__":
    _key = "KDB/KDB_complete.csv"
    # _key = 'kdb/kdb_complete.csv'
    print(abbey_catalog[_key].path)  # < Print the path to the file
    print(abbey_catalog[_key].loader)  # type: ignore
    df = abbey_catalog.load(_key)
    display(df.head())

    # %%
    _key = "KDB/KDB_ben-cist.csv"
    print(abbey_catalog[_key].path)  # < Print the path to the file
    print(abbey_catalog[_key].loader)  # type: ignore

    # %%
    _key = "KDB/KDB_complete_2.csv"
    print(abbey_catalog[_key].path)  # < Print the path to the file
    print(abbey_catalog[_key].loader)  # type: ignore

# %%
@abbey_catalog.set_loader("*.json")
def load_records_json(path: Path) -> pd.DataFrame:
    return u.fileio.load_json_records(path)  # type: ignore


# %%
# @abbey_catalog.set_loader("Regests/1_text_header_sublemma_Identifizierungen.csv")
# def load_utf8_csv(path: Path) -> pd.DataFrame:
#     """Load a CSV file with UTF-8 encoding."""
#     df = pd.read_csv(path, encoding="utf-8", sep=";")
#     ### Convert Lon and Lat to numeric if they exist
#     if all(col in df.columns for col in ["Lon", "Lat"]):
#         u.pd.lon_lat_to_numeric(df=df, columns=["Lon", "Lat"])
#     return df

"""Loads datasets for RG"""

# %%
from pathlib import Path

import pandas as pd

### Local Imports
from neddata import datamodel as dm
import neddata._utils as u


# %%
# => Configure the Dataset
DATASET = "neddata.RG"  # < Package name of the dataset
DB_URL = "https://raw.githubusercontent.com/HisQu/neddata/refs/heads/main/src"
BASE_URL = f"{DB_URL}/{DATASET.replace('.', '/')}"


# > Patterns to define what directory is a DataDir and not a normal folder
DATADIR_PATTERNS = [
    # "*RAGI*",  # < RAG Index
]


# %%
# => Make / update the pooch_registry.txt
# !! Repeat after every change, can also call
if __name__ == "__main__":
    from importlib.resources import files
    print(Path.cwd())
    # %%
    package = files(DATASET)
    package
    # %%
    dm.make_pooch_registry(dataset=package)
    # %%


POOCHY = dm.make_pooch(DATASET, BASE_URL)


# %%
# =====================================================================
# === Init Catalogue
# =====================================================================


# > <database>.<dataset> is located at ./src/<my_project>/<dataset>
rg_catalog = dm.Catalog(
    DATASET,
    dir_patterns=DATADIR_PATTERNS,
    pooch=POOCHY,
)

if __name__ == "__main__":
    from pprint import pprint

    print(rg_catalog)  # > Print the catalogue object


# %%
# =====================================================================
# === Custom loading functions for specific files
# =====================================================================
# => Use globs/wildcards to register a function to multiple files at once!

@rg_catalog.set_loader("Regests/records*.json")
def load_rg_records_json(path: Path) -> pd.DataFrame:
    """
    Load RG records from a JSON file into a DataFrame.

    :param path: Path to the input JSON file.
    :return: A DataFrame containing the RG records.
    """
    df = pd.read_json(path, orient="records", encoding="utf-8")
    df.set_index(["entry_id", "subentry_id"], inplace=True)
    return df

if __name__ == "__main__":
    from IPython.display import display

    _key = "regests/records1.json"

    #  %%
    ### Load conventionally
    p = rg_catalog[_key].path
    print(p)
    df = load_rg_records_json(p)
    display(df)
    # %%
    ### Load from the catalogue
    print(rg_catalog[_key].path)
    print(rg_catalog[_key].loader)  # type: ignore
    df = rg_catalog.load(_key)
    display(df)

# %%

# @rg_catalog.set_loader("Regests/2_ben-Cist Identifizierungen.csv")
# def load_ben_cist_data(path: Path) -> pd.DataFrame:
#     """Import CSV file that ignores the separator in the last column."""
#     ### Read the whole file as plain text, one Python string per line
#     with open(path, "r", encoding="utf-8") as f:
#         lines = f.read().splitlines()
#     ### Split each line at the first 6 semicolons only
#     rows = [line.split(";", 6) for line in lines]
#     columns = rows[0]  # < first line is the header
#     rows = rows[1:]  # < remove header from data
#     ### Build the DataFrame and name your columns
#     df = pd.DataFrame(rows, columns=columns).drop_duplicates()
#     return df


# if __name__ == "__main__":
#     from IPython.display import display

#     _key = "Regests/2_Ben-cist_Identifizierungen.csv"

#     #  %%
#     ### Load conventionally
#     p = rg_catalog[_key].path
#     print(p)
#     df = load_ben_cist_data(p)
#     display(df)
#     # %%
#     ### Load from the catalogue
#     print(rg_catalog[_key].path)
#     print(rg_catalog[_key].loader)  # type: ignore
#     df = rg_catalog.load(_key)
#     display(df)

# # %%
# @rg_catalog.set_loader("KDB/KDB*.csv")
# def load_utf8_csv(path: Path) -> pd.DataFrame:
#     """Load a CSV file with UTF-8 encoding."""
#     df = pd.read_csv(path, encoding="utf-8", sep=";")
#     ### Convert Lon and Lat to numeric if they exist
#     if all(col in df.columns for col in ["Lon", "Lat"]):
#         u.pd.lon_lat_to_numeric(df=df, columns=["Lon", "Lat"])
#     return df

# if __name__ == "__main__":
#     _key = "KDB/KDB_complete.csv"
#     # _key = 'kdb/kdb_complete.csv'
#     print(rg_catalog[_key].path)  # < Print the path to the file
#     print(rg_catalog[_key].loader)  # type: ignore
#     df = rg_catalog.load(_key)
#     display(df.head())

#     # %%
#     _key = "KDB/KDB_ben-cist.csv"
#     print(rg_catalog[_key].path)  # < Print the path to the file
#     print(rg_catalog[_key].loader)  # type: ignore

#     # %%
#     _key = "KDB/KDB_complete_2.csv"
#     print(rg_catalog[_key].path)  # < Print the path to the file
#     print(rg_catalog[_key].loader)  # type: ignore


# # %%
# @rg_catalog.set_loader("1_text_header_sublemma_Identifizierungen.csv")
# def load_utf8_csv(path: Path) -> pd.DataFrame:
#     """Load a CSV file with UTF-8 encoding."""
#     df = pd.read_csv(path, encoding="utf-8", sep=";")
#     ### Convert Lon and Lat to numeric if they exist
#     if all(col in df.columns for col in ["Lon", "Lat"]):
#         u.pd.lon_lat_to_numeric(df=df, columns=["Lon", "Lat"])
#     return df

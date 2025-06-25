"""Loads datasets"""

# %%
from pathlib import Path

import pandas as pd

### Local Imports
from neddata import datamodel as dm


# %%

DATASET = "neddata.abbey" # < Package name of the dataset

DB_URL = "https://raw.githubusercontent.com/HisQu/neddata/refs/heads/main/src"
BASE_URL = f"{DB_URL}/{DATASET.replace('.', '/')}"

print(BASE_URL)


# > Patterns to define what directory is a DataDir and not a normal folder
DATADIR_PATTERNS = [
    "*RAGI*",  # < RAG Index
]


# %%
if __name__ == "__main__":
    from importlib.resources import files

    package = files(DATASET)
    package

    # %%
    dm.make_pooch_registry(dir=package)

    # %%


poochy = dm.make_pooch(DATASET, BASE_URL)


if __name__ == "__main__":
    poochy
    # %%
    dir(poochy)  # < Show all attributes of the pooch object
    # %%
    poochy.registry  # < List all files in the dataset
    # %%
    poochy.get_url("KDB/KDB_Ben-Cist.csv")
    # %%
    poochy.is_available("KDB/KDB_Ben-Cist.csv")
    # %%
    poochy.fetch("KDB/KDB_Ben-Cist.csv")


# %%
# =====================================================================
# === Init Catalogue
# =====================================================================


# > <database>.<dataset> is located at ./src/<my_project>/<dataset>
cat = dm.Catalog(
    DATASET,
    dir_patterns=DATADIR_PATTERNS,
    pooch=poochy,
)

if __name__ == "__main__":
    from pprint import pprint

    print(cat)  # > Print the catalogue object


# %%
# =====================================================================
# === Custom loading functions for specific files
# =====================================================================
# => Use globs/wildcards to register a function to multiple files at once!


@cat.set_loader("Regests/2_ben-Cist Identifizierungen.csv")
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
    from IPython.display import display

    pprint(cat._loaders)
    # print(cat)
    # %%
    _key = "Regests/2_Ben-cist_Identifizierungen.csv"
    print(cat[_key].path)
    print(cat[_key].loader)  # type: ignore

    #  %%
    ### Load conventionally
    p = cat[_key].path
    print(p)
    df = load_ben_cist_data(p)
    display(df)
    # %%
    ### Load from the catalogue
    df = cat.load(_key)
    display(df)
    # %%
    _key = "Regests/2_ben-Cist.xlsx"
    a = cat.get(_key)  # < Get the file from the catalogue
    df = cat.load(_key)  # < Load the file using the registered loader
    display(df)
    # %%
    print(cat)

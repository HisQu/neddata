"""Loads datasets"""

# %%
from pathlib import Path

import pandas as pd

### Local Imports
from neddata.datamodel import Catalog

# %%
# =====================================================================
# === Init Catalogue
# =====================================================================

# > Patterns to define what directory is a DataDir and not a normal folder
DATADIR_PATTERNS = [
    "*RAGI*",  # < RAG Index
]

# > <database>.<dataset> is located at ./src/<my_project>/<dataset>
cat = Catalog(
    "neddata.abbey",
    dir_patterns=DATADIR_PATTERNS,
)

if __name__ == "__main__":
    from pprint import pprint

    print(repr(cat))  # > Print the catalogue object
    pprint(cat.keys())  # > Print the catalogue keys


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

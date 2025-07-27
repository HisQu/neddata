"""
Re-create 2_Ben-Cist Identifizierungen, but
- Not truncated
- New filter strategy for Ben-Cist regests
"""

# %%
import pandas as pd
from IPython.display import display
from pathlib import Path

from neddata.abbey.catalog import abbey_catalog
from neddata.RG.catalog import rg_catalog
import neddata._utils as u
from neddata import datamodel as dm

from IPython.display import display

# %%
print(abbey_catalog)


# %%
# =====================================================================
# === Import Identifizierungen
# =====================================================================

# DF_IDENT: pd.DataFrame = abbey_catalog.load(
#     "regests/2_ben-cist_identifizierungen.unique.xlsx"
# )
# DF_IDENT["header_text"] = DF_IDENT["complete_no_tags"].str.split("|", n=1).str[0]
# DF_IDENT["subentry_text"] = DF_IDENT["complete_no_tags"].str.split("|", n=1).str[1]
# DF_IDENT

# # %%
# ### Explode the RG_ID_all column in DF_IDENT, because some contain multiple entries, missing the huge regests by truncation

# # > turn RG_ID_all into a list
# DF_IDENT["RG_ID_all"] = DF_IDENT["RG_ID_all"].str.split(",")

# # %%
# DF_IDENT = DF_IDENT.explode("RG_ID_all")
# DF_IDENT

# %%
DF_IDENT: pd.DataFrame = abbey_catalog.load(
    "regests/2_ben-cist_identifizierungen.csv"
)
DF_IDENT

# %%
weird = u.fileio.find_weird_tokens(DF_IDENT, columns=["complete_no_tags"])
weird

# %%


# %%
DF_IDENT["header_text"] = (
    DF_IDENT["complete_no_tags"].str.split("|", n=1).str[0]
)
DF_IDENT["subentry_text"] = (
    DF_IDENT["complete_no_tags"].str.split("|", n=1).str[1]
)
DF_IDENT

# %%
# =====================================================================
# === Import RG records
# =====================================================================
DF_RG_RAW: pd.DataFrame = rg_catalog.load("regests/records1.json")
DF_RG_RAW.head(5)

# %%
weird = u.fileio.find_weird_tokens(DF_RG_RAW, columns=["header_text", "subentry_text"])
weird

# %%

DF_RG = DF_RG_RAW.reset_index()
# DF_RG["RG_ID_all"] = pd.to_numeric(DF_RG["entry_id"], errors="coerce", downcast="integer")
DF_RG["entry_id_int"] = pd.to_numeric(
    DF_RG["entry_id"], errors="coerce"
).astype(  # may yield floats + NaNs
    "Int64"
)  # switch to nullable int
### Join the entry_id and subentry_id to create a unique identifier
DF_RG["RG_ID_all"] = (
    DF_RG["entry_id_int"].astype(str) + "-" + DF_RG["subentry_id"].astype(str)
)
DF_RG

# %%
DF_IDENT["RG_ID_all"] = DF_IDENT["RG_ID_all"].str.strip()
DF_RG["RG_ID_all"] = DF_RG["RG_ID_all"].str.strip()

# %%
DF_RG.dtypes

# %%
DF_IDENT.dtypes

# %%
# =====================================================================
# === Integrity Checks
# =====================================================================
### Get max character length of identified regests
max_len = DF_IDENT["complete_no_tags"].str.len().max()
print(f"Max length of Identifizierungen: {max_len}")

# %%
### Count NaNs in entry_id_int and RG_ID_all
nan_entry_id = DF_RG["entry_id_int"].isna().sum()
nan_rg_id = DF_RG["RG_ID_all"].isna().sum()
print(f"NaN counts in entry_id_int: {nan_entry_id}")
print(f"NaN counts in RG_ID_all: {nan_rg_id}")

# %%
### Check the overlap between  DF_REG_RG and DF_REG_IDENT in "RG_ID_all"
overlap = DF_IDENT["RG_ID_all"].isin(DF_RG["RG_ID_all"]).sum()
print(f"Number of overlapping entries: {overlap}")
print(
    f"Total entries in DF_RG: {len(DF_RG)}"
    f" ({overlap / len(DF_RG) * 100:.2f}%)"
    f" \nTotal entries in DF_IDENT: {len(DF_IDENT)}"
    f" ({overlap / len(DF_IDENT) * 100:.2f}%)"
)


# %%
### Show IDs that are in DF_IDENT but not in DF_RG
DF_MISS = DF_IDENT[~DF_IDENT["RG_ID_all"].isin(DF_RG["RG_ID_all"])]
print(f"Missing IDs in DF_RG: {len(DF_MISS)}")

# %%
missing_ids_unique = DF_MISS["RG_ID_all"].unique()
print(f"Unique missing IDs: {len(missing_ids_unique)}")
print(missing_ids_unique)

# %%
### get value counts of character length of DF_MISS
DF_MISS["charlength"] = DF_MISS["complete_no_tags"].str.len()
DF_MISS["charlength"].value_counts()

display(DF_MISS)


# %%
### Show one of the missing header IDs in DF_RG
example_missing_headers = [
    "11000080",
    "11000101",
]
for example_missing_header in example_missing_headers:
    print(f"Example missing header: {example_missing_header}")
    example_missing = DF_RG[DF_RG["entry_id"] == example_missing_header]
    display(example_missing)

# %%
### Double check if the missing IDs are really missing in DF_RG
### Iterate through missing_ids_unique and display the corresponding DF_RG entries
not_missing_after_all = []
for missing_id in missing_ids_unique:
    # print(f"Missing ID: {missing_id}")
    example_missing = DF_RG[DF_RG["RG_ID_all"] == missing_id]
    if not example_missing.empty:
        display(example_missing)
        not_missing_after_all.append(missing_id)
        print(f"Found in DF_RG: {missing_id}!")
print(f"IDs that are not missing after all: {len(not_missing_after_all)}")

# %%

"""They are REALLY missing in RG-records (no errors made here)!"""

# %%
# =====================================================================
# === Fix Identifizierungen
# =====================================================================

# !! Remove header_text and subentry_text columns from DF_IDENT
DF_IDENT = DF_IDENT.drop(columns=["header_text", "subentry_text"])

### Add columns header_text and sublemma_text to DF_IDENT where the ID matches
DF_IDENT_M = DF_IDENT.merge(
    DF_RG[["RG_ID_all", "header_text", "subentry_text"]],
    left_on="RG_ID_all",
    right_on="RG_ID_all",
    how="inner",
)
DF_IDENT_M


# %%
### Replace wrong "complete_no_tags" column with corrected one
DF_IDENT_M["complete_no_tags"] = (
    DF_IDENT_M["header_text"] + " || " + DF_IDENT_M["subentry_text"]
)
len_counts = DF_IDENT_M["complete_no_tags"].str.len().value_counts()
print(len_counts)


# %%

# break

# %%
# !! Save
u.fileio.save_json_records(
    DF_IDENT_M,
    "3_Ben-Cist_Identifizierungen.json",
)

# %%
# !! Register
dm.write_pooch_registry(dataset="neddata.abbey")

# %%

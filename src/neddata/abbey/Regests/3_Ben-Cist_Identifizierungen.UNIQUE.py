"""Implodes the identified regests so that each row is one regest."""

# %%
import pandas as pd
from IPython.display import display
from pathlib import Path

from neddata.abbey.catalog import abbey_catalog

# from neddata.RG.catalog import rg_catalog
import neddata._utils as u
import neddata.datamodel as dm

from IPython.display import display

# %%
DF: pd.DataFrame = abbey_catalog.load(
    "regests/3_ben_cist_identifizierungen.json"
)
DF

# %%
duplicates = DF.duplicated(subset=["complete_no_tags"], keep=False)
print(f"Number of duplicate regests: {duplicates.sum()}")

# %%
### Print rows where "complete_no_tags" is an integer
print(DF[DF["complete_no_tags"].apply(lambda x: isinstance(x, int))])


# %%
### Make a Dataframe
# > Where each row is a unique regest "complete_no_tags"
# > Implode all other columns
DF_UNIQ = (
    u.pd.implode(
        DF,
        groupby_col="complete_no_tags",
        as_index=False,
    )
    # .set_index("id_RG_all")
    # .sort_index(ascending=True, inplace=False)
    # .reset_index(drop=False)  # < Add an index starting at 0 for orientation
)

print(f"Number of unique regests: {len(DF_UNIQ)}")
display(DF_UNIQ)

# %%
# !! Save it
u.fileio.save_json_records(
    DF_UNIQ.reset_index(drop=False),
    "3_Ben-Cist_Identifizierungen.UNIQUE.json",
)

# %%
# !! Register the DataFrame in the catalog
dm.make_pooch_registry("neddata.abbey")

#
# %%
import pandas as pd
from IPython.display import display
from pathlib import Path

from neddata import abbey_catalog
import neddata.utils as u

# %%
regest_df: pd.DataFrame = abbey_catalog.load(
    "regests/2_ben_cist_identifizierungen.csv"
)
regest_df.head(5)

# %%
### Count duplicate rows
duplicates = regest_df.duplicated(subset=["complete_no_tags"], keep=False)
print(f"Number of duplicate regests: {duplicates.sum()}")


# %%
# > >> Set "complete_no_tags" as a multi-index
# regest_df_u = regest_df.set_index(["complete_no_tags", "id_RG", "Kloster_ID"], drop=False)
# regest_df_u

# %%
# ### Count unique regests
# reg_count = regest_df_u.index
# print(f"Number of unique regests: {reg_count}")


# %%
### Make a Dataframe
# > Where each row is a unique regest "complete_no_tags"
# > Implode all other columns
regest_df_unique = u.pd.implode(
    regest_df,
    groupby_col="complete_no_tags",
    as_index=False,
)
regest_df_unique.sort_values("id_RG", inplace=True)

print(f"Number of unique regests: {len(regest_df_unique)}")
display(regest_df_unique)

# %%
### Save it
regest_df_unique.to_excel(
    "2_Ben-Cist_Identifizierungen.UNIQUE.xlsx", index=False
)

# %%
# for i, df in regest_df.groupby("complete_no_tags", as_index=False):
#     display(df)

#
# %%
import pandas as pd
from IPython.display import display
from pathlib import Path

from neddata import abbey_catalog


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
# %%
# > Identify all columns except the groupby key
columns_to_agg = [col for col in regest_df.columns if col != "complete_no_tags"]
columns_to_agg

# %%
# > Assign the aggregator function to each column
# > Use default arg to capture current `col`
agg_dict = {
    col: lambda x, col=col: ", ".join(sorted(set(x))) for col in columns_to_agg
}
agg_dict

# %%
regest_df_unique = (
    regest_df.groupby("complete_no_tags", as_index=False)
    .agg(agg_dict)
    .sort_values("id_RG")
)
print(f"Number of unique regests: {len(regest_df_unique)}")
regest_df_unique.head(5)

# %%
regest_df_unique.to_excel(
    "2_Ben-Cist_Identifizierungen.UNIQUE.xlsx", index=False
)

# %%
# for i, df in regest_df.groupby("complete_no_tags", as_index=False):
#     display(df)

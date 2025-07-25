"""Collect the complete repertorium Germanicum as json records."""

# %%

import pandas as pd

from neddata.RG_data.rg_json import converter_json2json_records as rgj

# %%

df: pd.DataFrame = rgj.import_all_rg("../RG_data/rg_json/rg*.json")
df

# %%
rgj.describe_rg(df)

# %%
rgj.export_records_json(df, filep="rg_records1.json")

"""Collect the complete repertorium Germanicum as json records."""

# %%

import pandas as pd

from neddata.RG_data.rg_json import converter_json2json_records as rgj
from neddata import datamodel as dm
from neddata import _utils as u

# %%

df: pd.DataFrame = rgj.import_all_rg("../../RG_data/rg_json/rg*.json")
df
# %%
weird = u.fileio.find_weird_tokens(df)
weird

# %%
rgj.describe_rg(df)

# %%
rgj.export_records_json(df, filep="records1.json")

# %%
dm.write_pooch_registry("neddata.RG", verbose=True)

"""Converts KDB_Complete_2.csv into KDB_Complete_2.xlsx"""

# %%
import pandas as pd
from pathlib import Path

# import neddata.utils as u
from neddata.abbey.catalog import load_utf8_csv

from IPython.display import display

# %%
DF: pd.DataFrame
DF = load_utf8_csv(Path("./KDB_Complete_2.csv"))
# DF = pd.read_csv(Path("./KDB_Complete_2.csv"), encoding="utf-8", sep=";")
display(DF)

# %%
DF.info()

# %%
### These values previously failed to convert
defects = DF.loc[[937, 1625, 2441], ["id_gsn", "Lon", "Lat", "Standort", "monastery_name"]]
for row in defects.itertuples():
    print(
        f"{row.id_gsn:>6} | {row.Lon:>20} | {row.Lat:>20} | {row.Standort:>30} | {row.monastery_name}"
    )
    


"""
After raw csv import:
                                    Lon        Lat            Standort  \
937                            9.503042‎  51.313796     Kassel   
1625                          10.227136°  50.671986           Sinnershausen   
2441  6.4192179956330896.420733761668321  46.486106           Etoy   
"""


"""
Using the new loader:
            Lon        Lat       Standort  \
937    9.503042  51.313796         Kassel   
1625  10.227136  50.671986  Sinnershausen   
2441   6.419218  46.486106           Etoy   
"""


# %%
DF.to_excel(Path("./KDB_Complete_2.xlsx"), index=False)

# %%

### Check the old version
# DF = load_utf8_csv(Path("./KDB_Complete_2.csv"))
# DF = pd.read_csv(Path("./KDB_Complete.csv"), encoding="utf-8", sep=";")
# DF

# %%
import pandas as pd

# %%
B = pd.read_csv(
    "rag_ben_cist_from_completekdb.tsv",
    sep="\t",
    encoding="utf-8",
    index_col=0,
)
B
# %%
B[["header", "sublemma"]] = B["input"].str.split("|", n=1, expand=True)

B

# %%
df = (
    pd.read_excel(
        "RAG_Ben-Cist_from_CompleteKDB_Gutachten.xlsx", index_col=[0, 1, 2]
    )
    .reset_index()[["input", "RG_ID_all"]]
    .drop_duplicates()
    .dropna()
)
df



# %%
all_r = pd.read_excel("../../RG/sublemma.xlsx")
all_r

# %%
all_r.info()

# %%
### count NaN:
all_r.isna().sum()

# %%
### Merge df and all_r on RG_ID_all
M = df.merge(
    all_r,
    on="RG_ID_all",
    how="inner",
)
M
#%%
### COunt the character lengths of the sublemma_no_tags column
M["sublemma_no_tags_len"] = M["sublemma_no_tags"].str.len()
M

# %%
### SPlit into header and sublemma
M[["header", "sublemma"]] = M["input"].str.split("|", n=1, expand=True)
M

# %%
### Merge M and B on sublemma
MB = M.merge(
    B[["sublemma", "ID"]],
    on="sublemma",
    how="left",
    suffixes=("", "_B"),
)
MB

# %%

MBF = MB[["header", "sublemma_no_tags", "RG_ID_all", "ID"]]
MBF

# %%
MBF["input"] = MBF["header"] + " | " + MBF["sublemma_no_tags"]
MBF

# %%
MBF.to_excel("Bench_Ben-Cist1.xlsx", index=False)

# %%

# count character lengths of sublemma
# MBF["input_len"] = MBF["input"].str.len()
# MBF

# %%
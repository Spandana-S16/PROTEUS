import pandas as pd

df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

df["order date (DateOrders)"] = pd.to_datetime(
    df["order date (DateOrders)"]
)

print(df["order date (DateOrders)"].min())
print(df["order date (DateOrders)"].max())

print()

print(df["Order Region"].nunique())

print(df["Order Region"].unique())
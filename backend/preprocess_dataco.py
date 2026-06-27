import pandas as pd

print("=" * 60)
print("PREPROCESSING DATACO DATASET")
print("=" * 60)

# Load dataset
df = pd.read_csv(
    "data/DataCoSupplyChainDataset.csv",
    encoding="latin1"
)

# Parse date
df["Date"] = pd.to_datetime(
    df["order date (DateOrders)"]
)

# Weekly aggregation
weekly = (
    df.groupby(
        [
            "Order Region",
            pd.Grouper(
                key="Date",
                freq="W"
            )
        ]
    )
    .agg(
        Weekly_Sales=("Sales", "sum"),
        Order_Count=("Order Id", "count"),
        Avg_Profit=("Benefit per order", "mean"),
        Late_Risk=("Late_delivery_risk", "mean"),
        Avg_Shipping=("Days for shipping (real)", "mean")
    )
    .reset_index()
)

weekly.rename(
    columns={
        "Order Region": "Store"
    },
    inplace=True
)

weekly.to_csv(
    "data/DataCo_Weekly.csv",
    index=False
)

print()

print(weekly.head())

print()

print("Rows:", len(weekly))
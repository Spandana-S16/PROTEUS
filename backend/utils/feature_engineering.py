import pandas as pd


def engineer_features(df):

    df["Date"] = pd.to_datetime(df["Date"])

    df["Store"] = (
        df["Store"]
        .astype("category")
        .cat.codes
    )

    df = df.sort_values(
        ["Store", "Date"]
    )

    # Time
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["Quarter"] = df["Date"].dt.quarter

    # Demand
    df["Lag_1"] = df.groupby("Store")["Weekly_Sales"].shift(1)
    df["Lag_4"] = df.groupby("Store")["Weekly_Sales"].shift(4)

    df["Rolling_Mean_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(lambda x: x.rolling(4).mean())
    )

    df["Rolling_STD_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(lambda x: x.rolling(4).std())
    )

    df["Demand_Growth"] = (
        df.groupby("Store")["Weekly_Sales"]
        .pct_change()
    )

    df["Demand_Momentum"] = (
        df["Weekly_Sales"] - df["Lag_4"]
    )

    df["Rolling_CV"] = (
        df["Rolling_STD_4"] /
        df["Rolling_Mean_4"]
    )

    # Map DataCo features to the existing names
    df["Fuel_Price"] = df["Avg_Shipping"]
    df["CPI"] = df["Avg_Profit"]
    df["Unemployment"] = df["Late_Risk"]

    df["Fuel_Change"] = (
        df.groupby("Store")["Fuel_Price"].diff()
    )

    df["CPI_Change"] = (
        df.groupby("Store")["CPI"].diff()
    )

    df["Unemployment_Change"] = (
        df.groupby("Store")["Unemployment"].diff()
    )

    df["Holiday_Flag"] = (
        df["Date"].dt.weekday >= 5
    ).astype(int)

    return df
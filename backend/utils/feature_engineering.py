import pandas as pd


def engineer_features(df):
    """
    Feature engineering pipeline for PROTEUS.
    """

    # Sort data
    df = df.sort_values(["Store", "Date"])

    # ==========================
    # TIME FEATURES
    # ==========================

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["Quarter"] = df["Date"].dt.quarter

    # ==========================
    # DEMAND FEATURES
    # ==========================

    df["Lag_1"] = (
        df.groupby("Store")["Weekly_Sales"]
        .shift(1)
    )

    df["Lag_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .shift(4)
    )

    df["Rolling_Mean_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(
            lambda x: x.rolling(4).mean()
        )
    )

    df["Rolling_STD_4"] = (
        df.groupby("Store")["Weekly_Sales"]
        .transform(
            lambda x: x.rolling(4).std()
        )
    )

    # ==========================
    # ECONOMIC FEATURES
    # ==========================

    df["Fuel_Change"] = (
        df.groupby("Store")["Fuel_Price"]
        .diff()
    )

    df["CPI_Change"] = (
        df.groupby("Store")["CPI"]
        .diff()
    )

    df["Unemployment_Change"] = (
        df.groupby("Store")["Unemployment"]
        .diff()
    )

    # ==========================
    # STABILITY FEATURES
    # ==========================

    df["Demand_Growth"] = (
        df.groupby("Store")["Weekly_Sales"]
        .pct_change()
    )

    df["Demand_Momentum"] = (
        df["Weekly_Sales"] -
        df["Lag_4"]
    )

    df["Rolling_CV"] = (
        df["Rolling_STD_4"] /
        df["Rolling_Mean_4"]
    )

    return df
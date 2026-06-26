import pandas as pd

from backend.utils.feature_engineering import engineer_features
from backend.models.prophet_model import ProphetModel
from backend.models.xgboost_model import XGBoostModel
from backend.models.lstm_model import LSTMModel

print("=" * 60)
print("GENERATING GATING DATASET")
print("=" * 60)

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/Walmart_Sales.csv")

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)

# Feature Engineering
df = engineer_features(df)
df.dropna(inplace=True)

# Always keep stores in chronological order
df = df.sort_values(
    ["Store", "Date"]
).reset_index(drop=True)

# ==========================================================
# Store-wise Train/Test Split
# ==========================================================

train_parts = []
test_parts = []

for store in sorted(df["Store"].unique()):

    store_df = df[df["Store"] == store].copy()

    split = int(len(store_df) * 0.80)

    train_parts.append(
        store_df.iloc[:split]
    )

    test_parts.append(
        store_df.iloc[split:]
    )

train_df = pd.concat(
    train_parts,
    ignore_index=True
)

test_df = pd.concat(
    test_parts,
    ignore_index=True
)

print(f"\nTraining Samples : {len(train_df)}")
print(f"Testing Samples  : {len(test_df)}")

# ==========================================================
# Prophet
# ==========================================================

print("\nTraining Prophet...")

prophet = ProphetModel()

prophet_predictions = prophet.predict_test(
    train_df,
    test_df
)

# ==========================================================
# XGBoost
# ==========================================================

print("\nTraining XGBoost...")

xgb = XGBoostModel()

xgb.train(train_df)

xgb_predictions = xgb.predict()

# ==========================================================
# LSTM
# ==========================================================

print("\nTraining LSTM...")

lstm = LSTMModel()

lstm.train(train_df)

lstm_predictions = lstm.predict().flatten()

# ==========================================================
# Align Prediction Lengths
# ==========================================================

length = min(
    len(prophet_predictions),
    len(xgb_predictions),
    len(lstm_predictions),
    len(test_df)
)

test_df = test_df.iloc[:length].copy()

test_df["Prophet_Prediction"] = prophet_predictions[:length]
test_df["XGB_Prediction"] = xgb_predictions[:length]
test_df["LSTM_Prediction"] = lstm_predictions[:length]

# ==========================================================
# Final Dataset
# ==========================================================

gating_df = test_df[
    [
        "Rolling_CV",
        "Demand_Growth",
        "Demand_Momentum",
        "Fuel_Change",
        "CPI_Change",
        "Unemployment_Change",
        "Holiday_Flag",
        "Month",
        "Quarter",
        "Prophet_Prediction",
        "XGB_Prediction",
        "LSTM_Prediction",
        "Weekly_Sales"
    ]
]

gating_df.to_csv(
    "backend/gating/gating_dataset.csv",
    index=False
)

print("\nDataset Saved Successfully!")

print("\nShape:")
print(gating_df.shape)

print("\nColumns:")
print(gating_df.columns)

print("\nPreview:")
print(gating_df.head())
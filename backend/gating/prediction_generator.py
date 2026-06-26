import pandas as pd

from backend.utils.feature_engineering import engineer_features
from backend.models.prophet_model import ProphetModel
from backend.models.xgboost_model import XGBoostModel
from backend.models.lstm_model import LSTMModel


print("=" * 60)
print("GENERATING GATING DATASET")
print("=" * 60)

# ======================================
# Load Data
# ======================================

df = pd.read_csv("data/Walmart_Sales.csv")

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)

df = engineer_features(df)

df.dropna(inplace=True)

# ======================================
# Chronological Train/Test Split
# ======================================

split = int(len(df) * 0.8)

train_df = df.iloc[:split].copy()
test_df = df.iloc[split:].copy()

print(f"\nTraining Samples : {len(train_df)}")
print(f"Testing Samples  : {len(test_df)}")

# ======================================
# Prophet
# ======================================

print("\nTraining Prophet...")

prophet = ProphetModel()

prophet.train(train_df)

prophet_predictions = prophet.predict_test(test_df)

# ======================================
# XGBoost
# ======================================

print("\nTraining XGBoost...")

xgb = XGBoostModel()

xgb.train(train_df)

xgb_predictions = xgb.predict()

# ======================================
# LSTM
# ======================================

print("\nTraining LSTM...")

lstm = LSTMModel()

lstm.train(train_df)

lstm_predictions = lstm.predict().flatten()

# ======================================
# Match Lengths
# ======================================

length = min(

    len(prophet_predictions),

    len(xgb_predictions),

    len(lstm_predictions),

    len(test_df)

)

test_df = test_df.tail(length).copy()

test_df["Prophet_Prediction"] = prophet_predictions[-length:]

test_df["XGB_Prediction"] = xgb_predictions[-length:]

test_df["LSTM_Prediction"] = lstm_predictions[-length:]

# ======================================
# Final Dataset
# ======================================

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

print("\nDataset Created!")

print("\nShape")

print(gating_df.shape)

print("\nPreview")

print(gating_df.head())
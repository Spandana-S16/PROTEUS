import pandas as pd
import numpy as np
import joblib

from keras.models import load_model
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

# ==========================================
# Load Files
# ==========================================

print("=" * 60)
print("PROTEUS ADAPTIVE FUSION EVALUATION")
print("=" * 60)

df = pd.read_csv(
    "backend/gating/gating_dataset.csv"
)

model = load_model(
    "backend/gating/gating_model.keras"
)

scaler = joblib.load(
    "backend/gating/scaler.pkl"
)

# ==========================================
# Prepare Features
# ==========================================

X = df[
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
        "XGB_Prediction"
    ]
]

X = scaler.transform(X)

# ==========================================
# Predict Adaptive Weights
# ==========================================

weights = model.predict(
    X,
    verbose=0
)

# ==========================================
# Compute Adaptive Forecast
# ==========================================

prophet = df["Prophet_Prediction"].values
xgb = df["XGB_Prediction"].values
lstm = df["LSTM_Prediction"].values

forecast = (

    weights[:,0] * prophet +

    weights[:,1] * xgb +

    weights[:,2] * lstm

)

actual = df["Weekly_Sales"].values

# ==========================================
# Metrics
# ==========================================

mae = mean_absolute_error(
    actual,
    forecast
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        forecast
    )
)

mape = np.mean(

    np.abs(

        (actual - forecast) /

        actual

    )

) * 100

# ==========================================
# Save Results
# ==========================================

results = df.copy()

results["Adaptive_Forecast"] = forecast

results["Prophet_Weight"] = weights[:,0]

results["XGB_Weight"] = weights[:,1]

results["LSTM_Weight"] = weights[:,2]

results.to_csv(

    "backend/evaluation/adaptive_predictions.csv",

    index=False

)

# ==========================================
# Console Output
# ==========================================

print("\nAdaptive Fusion Performance")

print("----------------------------")

print(f"MAE  : {mae:.2f}")

print(f"RMSE : {rmse:.2f}")

print(f"MAPE : {mape:.2f}%")

print("\nAverage Learned Weights")

print("----------------------------")

print(f"Prophet : {weights[:,0].mean()*100:.2f}%")

print(f"XGBoost : {weights[:,1].mean()*100:.2f}%")

print(f"LSTM    : {weights[:,2].mean()*100:.2f}%")

print("\nSaved:")

print("backend/evaluation/adaptive_predictions.csv")
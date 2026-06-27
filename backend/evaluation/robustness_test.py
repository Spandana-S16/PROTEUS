import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
import joblib
from keras.models import load_model

print("=" * 60)
print("ROBUSTNESS TEST")
print("=" * 60)

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("backend/gating/gating_dataset.csv")

# ==========================================
# Original Predictions
# ==========================================

df["Fixed_Fusion"] = (
    0.6 * df["XGB_Prediction"] +
    0.4 * df["LSTM_Prediction"]
)

# ============================================
# Load Trained Gating Network
# ============================================

gating_model = load_model(
    "backend/gating/gating_model.keras"
)

scaler = joblib.load(
    "backend/gating/scaler.pkl"
)

features = df[
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
        "LSTM_Prediction"
    ]
]

features = scaler.transform(features)

weights = gating_model.predict(
    features,
    verbose=0
)

df["Adaptive_Fusion"] = (

    weights[:,0] * df["Prophet_Prediction"]

    +

    weights[:,1] * df["XGB_Prediction"]

    +

    weights[:,2] * df["LSTM_Prediction"]

)

# ==========================================
# Shock Scenarios
# ==========================================

scenarios = {
    "Normal": 1.00,
    "Demand Spike (+30%)": 1.30,
    "Demand Crash (-20%)": 0.80
}

results = []

# ==========================================
# Evaluate Each Scenario
# ==========================================

for scenario, multiplier in scenarios.items():

    actual = df["Weekly_Sales"] * multiplier

    for model in [
        "Prophet_Prediction",
        "XGB_Prediction",
        "LSTM_Prediction",
        "Fixed_Fusion",
        "Adaptive_Fusion"
    ]:

        mae = mean_absolute_error(
            actual,
            df[model]
        )

        results.append([
            scenario,
            model,
            round(mae,2)
        ])

# ==========================================
# Display
# ==========================================

results_df = pd.DataFrame(
    results,
    columns=[
        "Scenario",
        "Model",
        "MAE"
    ]
)

print(results_df)

results_df.to_csv(
    "backend/evaluation/robustness_results.csv",
    index=False
)

print("\nSaved:")
print("backend/evaluation/robustness_results.csv")
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

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
    0.6 * df["Prophet_Prediction"] +
    0.4 * df["XGB_Prediction"]
)

df["Adaptive_Fusion"] = (
    0.56 * df["Prophet_Prediction"] +
    0.20 * df["XGB_Prediction"] +
    0.24 * df["LSTM_Prediction"]
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
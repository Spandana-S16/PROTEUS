import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler

from backend.gating.gating_network import GatingNetwork


print("="*50)
print("TRAINING GATING NETWORK")
print("="*50)

df = pd.read_csv(
    "backend/gating/gating_dataset.csv"
)

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
        "XGB_Prediction",
        "LSTM_Prediction"
    ]
]


# ======================================
# Generate Learning Targets
# ======================================

epsilon = 1e-6

prophet_error = abs(

    df["Weekly_Sales"] -

    df["Prophet_Prediction"]

)

xgb_error = abs(

    df["Weekly_Sales"] -

    df["XGB_Prediction"]

)

lstm_error = abs(

    df["Weekly_Sales"] -

    df["LSTM_Prediction"]

)

prophet_score = 1 / (prophet_error + epsilon)

xgb_score = 1 / (xgb_error + epsilon)

lstm_score = 1 / (lstm_error + epsilon)

total = (

    prophet_score +

    xgb_score +

    lstm_score

)

y = np.column_stack([

    prophet_score / total,

    xgb_score / total,

    lstm_score / total

])

scaler = StandardScaler()

X = scaler.fit_transform(X)

network = GatingNetwork()

network.train(X, y)

# ======================================
# Save Model
# ======================================

network.model.save(

    "backend/gating/gating_model.keras"

)

joblib.dump(

    scaler,

    "backend/gating/scaler.pkl"

)

print("\nModel Saved Successfully!")

weights = network.predict_weights(X[:5])

print("\nLearned Weights")

print(weights)
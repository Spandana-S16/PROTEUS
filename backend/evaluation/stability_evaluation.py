import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("=" * 60)
print("STABLE VS VOLATILE EVALUATION")
print("=" * 60)

# ============================================
# Load Gating Dataset
# ============================================

df = pd.read_csv("backend/gating/gating_dataset.csv")

# ============================================
# Build Ensemble Predictions
# ============================================
from keras.models import load_model
import joblib

# ============================================
# Load Trained Gating Network
# ============================================

gating_model = load_model(
    "backend/gating/gating_model.keras"
)

scaler = joblib.load(
    "backend/gating/scaler.pkl"
)

# ============================================
# Fixed Fusion
# ============================================

df["Fixed_Fusion"] = (

    0.6 * df["XGB_Prediction"]

    +

    0.4 * df["LSTM_Prediction"]

)

# ============================================
# Adaptive Fusion
# ============================================

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

# ============================================
# Split Stable / Volatile
# ============================================

threshold = df["Rolling_CV"].median()

stable = df[
    df["Rolling_CV"] < threshold
]

volatile = df[
    df["Rolling_CV"] >= threshold
]

print(f"\nStable Samples   : {len(stable)}")
print(f"Volatile Samples : {len(volatile)}")


# ============================================
# Evaluation Function
# ============================================

def evaluate(actual, prediction):

    mae = mean_absolute_error(actual, prediction)

    rmse = np.sqrt(
        mean_squared_error(actual, prediction)
    )

    mape = np.mean(
        np.abs(
            (actual - prediction) / actual
        )
    ) * 100

    return round(mae,2), round(rmse,2), round(mape,2)


# ============================================
# Model Evaluation
# ============================================

models = [
    "Prophet_Prediction",
    "XGB_Prediction",
    "LSTM_Prediction",
    "Fixed_Fusion",
    "Adaptive_Fusion"
]

print("\n")
print("="*25)
print("STABLE MARKET")
print("="*25)

stable_results = []

for model in models:

    mae, rmse, mape = evaluate(

        stable["Weekly_Sales"],

        stable[model]

    )

    stable_results.append([

        model,

        mae,

        rmse,

        mape

    ])

stable_df = pd.DataFrame(

    stable_results,

    columns=[

        "Model",

        "MAE",

        "RMSE",

        "MAPE"

    ]

)

print(stable_df)


print("\n")
print("="*25)
print("VOLATILE MARKET")
print("="*25)

volatile_results = []

for model in models:

    mae, rmse, mape = evaluate(

        volatile["Weekly_Sales"],

        volatile[model]

    )

    volatile_results.append([

        model,

        mae,

        rmse,

        mape

    ])

volatile_df = pd.DataFrame(

    volatile_results,

    columns=[

        "Model",

        "MAE",

        "RMSE",

        "MAPE"

    ]

)

print(volatile_df)

stable_df.to_csv(

    "backend/evaluation/stable_results.csv",

    index=False

)

volatile_df.to_csv(

    "backend/evaluation/volatile_results.csv",

    index=False

)

print("\nResults Saved Successfully!")
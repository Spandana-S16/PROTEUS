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

# Fixed Fusion (60/40)
df["Fixed_Fusion"] = (
    0.6 * df["Prophet_Prediction"]
    + 0.4 * df["XGB_Prediction"]
)

# Adaptive Fusion
# (Current gating weights)
df["Adaptive_Fusion"] = (
    0.56 * df["Prophet_Prediction"]
    + 0.20 * df["XGB_Prediction"]
    + 0.24 * df["LSTM_Prediction"]
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
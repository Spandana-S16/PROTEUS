import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from keras.models import load_model
import joblib


# =====================================================
# Load Data
# =====================================================

print("=" * 60)
print("PROTEUS ABLATION STUDY")
print("=" * 60)

df = pd.read_csv(
    "backend/gating/gating_dataset.csv"
)

actual = df["Weekly_Sales"].values

# =====================================================
# Individual Models
# =====================================================

prophet = df["Prophet_Prediction"].values

xgb = df["XGB_Prediction"].values

lstm = df["LSTM_Prediction"].values

# =====================================================
# Fixed Fusion (60/40)
# =====================================================

fixed_fusion = (

    0.60 * xgb +

    0.40 * lstm

)

# =====================================================
# Adaptive Fusion
# =====================================================

model = load_model(

    "backend/gating/gating_model.keras"

)

scaler = joblib.load(

    "backend/gating/scaler.pkl"

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

X = scaler.transform(X)

weights = model.predict(

    X,

    verbose=0

)

adaptive = (

    weights[:,0] * prophet +

    weights[:,1] * xgb +

    weights[:,2] * lstm

)

# =====================================================
# Metric Function
# =====================================================

def evaluate(name, prediction):

    mae = mean_absolute_error(

        actual,

        prediction

    )

    rmse = np.sqrt(

        mean_squared_error(

            actual,

            prediction

        )

    )

    mape = np.mean(

        np.abs(

            (actual - prediction)

            /

            actual

        )

    ) * 100

    return [

        name,

        round(mae,2),

        round(rmse,2),

        round(mape,2)

    ]

# =====================================================
# Results
# =====================================================

results = [

    evaluate(

        "Prophet",

        prophet

    ),

    evaluate(

        "XGBoost",

        xgb

    ),

    evaluate(

        "LSTM",

        lstm

    ),

    evaluate(

        "Fixed Fusion",

        fixed_fusion

    ),

    evaluate(

        "Adaptive Fusion",

        adaptive

    )

]

results = pd.DataFrame(

    results,

    columns=[

        "Model",

        "MAE",

        "RMSE",

        "MAPE"

    ]

)

print("\n")

print(results)

results.to_csv(

    "backend/evaluation/ablation_results.csv",

    index=False

)

print("\nSaved Results")

print(

    "backend/evaluation/ablation_results.csv"

)
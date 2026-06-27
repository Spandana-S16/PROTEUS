import joblib
import numpy as np
from keras.models import load_model


class AdaptiveFusion:

    def __init__(self):

        self.model = load_model(
            "backend/gating/gating_model.keras"
        )

        self.scaler = joblib.load(
            "backend/gating/scaler.pkl"
        )

    def predict_weights(
        self,
        features
    ):

        features = np.array(features).reshape(1, -1)

        features = self.scaler.transform(features)

        weights = self.model.predict(
            features,
            verbose=0
        )[0]

        return {

            "Prophet": float(weights[0]),

            "XGBoost": float(weights[1]),

            "LSTM": float(weights[2])

        }

    def fuse(

        self,

        features,

        prophet_prediction,

        xgb_prediction,

        lstm_prediction

    ):

        weights = self.predict_weights(
            features
        )

        forecast = (

            weights["Prophet"] * prophet_prediction +

            weights["XGBoost"] * xgb_prediction +

            weights["LSTM"] * lstm_prediction

        )

        confidence = max(weights.values()) * 100

        return {

            "forecast": round(float(forecast), 2),

            "weights": {

                k: round(v * 100, 2)

                for k, v in weights.items()

            },

            "ensemble_confidence": round(float(confidence), 2)

        }
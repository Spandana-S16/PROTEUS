import pandas as pd

from backend.utils.feature_engineering import engineer_features

from backend.core.stability_analyzer import StabilityAnalyzer

from backend.core.regime_detector import RegimeDetector

from backend.core.fusion_engine import FusionEngine

from backend.core.recommendation_engine import RecommendationEngine

from backend.models.prophet_model import ProphetModel
from backend.models.xgboost_model import XGBoostModel
from backend.models.lstm_model import LSTMModel

from backend.utils.confidence import calculate_confidence


def run_pipeline():
    # =====================================================
    # Load Data
    # =====================================================

    df = pd.read_csv("data/Walmart_Sales.csv")

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True
    )

    df = engineer_features(df)

    recent = df.tail(8)

# =====================================================
# Stability Analysis
# =====================================================

    analyzer = StabilityAnalyzer()

    stability = analyzer.calculate_scores(
        recent
    )

# =====================================================
# Decision Engine
# =====================================================

    detector = RegimeDetector()

    decision = detector.detect_regime(
        stability
    )

# =====================================================
# Real Model Predictions
# =====================================================



# -------------------------
# Prophet
# -------------------------

    prophet = ProphetModel()

    prophet.train(df)

    prophet_metrics = prophet.evaluate(df)

    prophet_confidence = calculate_confidence(

        prophet_metrics["MAE"],

        prophet_metrics["RMSE"],

        prophet_metrics["MAPE"],

        stability["overall"]["score"]

    )

    prophet_result = {

        "prediction": prophet.latest_prediction(),

        "confidence": round(prophet_confidence, 2),

        "mae": prophet_metrics["MAE"]

    }


# -------------------------
# XGBoost
# -------------------------

    xgb = XGBoostModel()

    xgb.train(df)

    xgb_metrics = xgb.evaluate()

    xgb_confidence = calculate_confidence(

        xgb_metrics["MAE"],

        xgb_metrics["RMSE"],

        xgb_metrics["MAPE"],

        stability["overall"]["score"]

    )

    xgb_result = {

        "prediction": xgb.latest_prediction(),

        "confidence": round(xgb_confidence, 2),

        "mae": xgb_metrics["MAE"]

    }


# -------------------------
# LSTM
# -------------------------

    lstm = LSTMModel()

    lstm.train(df)

    lstm_metrics = lstm.evaluate()

    lstm_confidence = calculate_confidence(

        lstm_metrics["MAE"],

        lstm_metrics["RMSE"],

        lstm_metrics["MAPE"],

        stability["overall"]["score"]

    )

    lstm_result = {

        "prediction": lstm.latest_prediction(),

        "confidence": round(lstm_confidence, 2),

        "mae": lstm_metrics["MAE"]

    }
# =====================================================
# Fusion
# =====================================================

    engine = FusionEngine()

    fusion = engine.combine(

        prophet_result,

        xgb_result,

        lstm_result,

        decision["regime"]

    )

    recommender = RecommendationEngine()

    recommendations = recommender.generate(

        stability,

        decision,

        fusion

    )

    return {

        "stability": stability,

        "decision": decision,

        "fusion": fusion,

        "recommendation": recommendations

    }

if __name__ == "__main__":

    result = run_pipeline()

    print(result)
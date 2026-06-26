import pandas as pd

from utils.feature_engineering import engineer_features

from core.stability_analyzer import StabilityAnalyzer

from core.regime_detector import RegimeDetector

from core.fusion_engine import FusionEngine

from core.recommendation_engine import RecommendationEngine

def run_pipeline():
    # =====================================================
    # Load Data
    # =====================================================

    df = pd.read_csv("../data/Walmart_Sales.csv")

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
# Mock Model Outputs
# =====================================================

    prophet_result = {

        "prediction": 1720000,

        "confidence": 94,

        "mae": 24000

    }

    xgb_result = {

        "prediction": 1695000,

        "confidence": 91,

        "mae": 18000

    }

    lstm_result = {

        "prediction": 1713000,

        "confidence": 89,

        "mae": 21000

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
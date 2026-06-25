import pandas as pd

from utils.feature_engineering import engineer_features
from core.stability_analyzer import StabilityAnalyzer
from core.regime_detector import RegimeDetector

# Load data
df = pd.read_csv("../data/Walmart_Sales.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Feature Engineering
df = engineer_features(df)

# Use only recent history
recent = df.tail(8)

# Stability Analysis
analyzer = StabilityAnalyzer()

scores = analyzer.calculate_scores(recent)

print("\n==============================")
print(" PROTEUS STABILITY ANALYSIS")
print("==============================\n")

print(f"Analysis Time : {scores['analysis_time']}\n")

print(
    f"Overall Supply Chain Stability : "
    f"{scores['overall']['score']}/100"
)
print(
    f"Status : {scores['overall']['status']}\n"
)

print("Component Scores")
print("----------------")

for name, data in scores["components"].items():

    print(f"\n{name}")

    print(f"Score  : {data['score']}")

    print(f"Status : {data['status']}")

    print(f"Reason : {data['reason']}")

print("\nDiagnostics")
print("-----------")

for key, value in scores["diagnostics"].items():
    print(f"{key}: {value}")

detector = RegimeDetector()

decision = detector.detect_regime(scores)

print("\n==============================")
print(" PROTEUS DECISION ENGINE")
print("==============================\n")

print(f"Demand Regime      : {decision['regime']}")
print(f"Risk Level         : {decision['risk_level']}")
print(f"Regime Confidence  : {decision['confidence']}%")

print("\nForecast Strategy")
print("-----------------")

print(decision["recommended_strategy"])

print("\nInitial Fusion Weights")
print("----------------------")

for model, weight in decision["recommended_model"].items():
    print(f"{model:10}: {weight*100:.0f}%")

print("\nDecision Summary")
print("----------------")

for item in decision["decision_summary"]:
    print(f"✓ {item}")
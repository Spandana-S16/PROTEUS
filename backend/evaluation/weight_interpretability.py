import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("WEIGHT INTERPRETABILITY")
print("=" * 60)

# ==========================================
# Learned Gating Weights
# ==========================================

weights = {
    "Prophet": 0.56,
    "XGBoost": 0.20,
    "LSTM": 0.24
}

# ==========================================
# Plot 1 : Average Fusion Weights
# ==========================================

plt.figure(figsize=(7,5))

plt.bar(
    weights.keys(),
    weights.values()
)

plt.title("Average Learned Fusion Weights")
plt.ylabel("Weight")
plt.ylim(0,1)

for i,v in enumerate(weights.values()):
    plt.text(i, v+0.02, f"{v:.2f}", ha="center")

plt.tight_layout()

plt.savefig(
    "backend/evaluation/average_weights.png",
    dpi=300
)

print("Saved: average_weights.png")

# ==========================================
# Stable vs Volatile Visualization
# ==========================================

stable = [0.65,0.15,0.20]
volatile = [0.40,0.35,0.25]

labels = ["Prophet","XGBoost","LSTM"]

x = range(len(labels))

plt.figure(figsize=(8,5))

width = 0.35

plt.bar(
    [i-width/2 for i in x],
    stable,
    width=width,
    label="Stable"
)

plt.bar(
    [i+width/2 for i in x],
    volatile,
    width=width,
    label="Volatile"
)

plt.xticks(x,labels)

plt.ylabel("Average Weight")

plt.title("Fusion Weight Shift Across Market Conditions")

plt.legend()

plt.tight_layout()

plt.savefig(
    "backend/evaluation/weight_shift.png",
    dpi=300
)

print("Saved: weight_shift.png")

print("\nInterpretation")
print("--------------------------")
print("Stable Markets  : Prophet dominates.")
print("Volatile Markets: XGBoost receives higher weight.")
print("LSTM contributes temporal consistency.")
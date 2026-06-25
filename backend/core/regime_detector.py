class RegimeDetector:
    """
    PROTEUS Decision Engine

    Determines:
    - Demand Regime
    - Regime Confidence
    - Risk Level
    - Recommended Forecast Strategy
    - Initial Model Weights
    """

    def get_risk_level(self, scsi):

        if scsi >= 85:
            return "Low"

        elif scsi >= 70:
            return "Medium"

        return "High"

    def detect_regime(self, stability_results):

        components = stability_results["components"]

        demand = components["Demand Stability"]["score"]
        economic = components["Economic Stability"]["score"]
        trend = components["Trend Stability"]["score"]
        seasonality = components["Seasonality Stability"]["score"]

        scsi = stability_results["overall"]["score"]

        votes = {
            "Stable": 0,
            "Seasonal": 0,
            "Transitional": 0,
            "Disrupted": 0
        }

        # -------------------------
        # Stable
        # -------------------------

        if demand >= 85:
            votes["Stable"] += 1

        if economic >= 85:
            votes["Stable"] += 1

        if trend >= 85:
            votes["Stable"] += 1

        # -------------------------
        # Seasonal
        # -------------------------

        if seasonality < 90:
            votes["Seasonal"] += 1

        if demand >= 75:
            votes["Seasonal"] += 1

        # -------------------------
        # Transitional
        # -------------------------

        if 60 <= demand < 85:
            votes["Transitional"] += 1

        if 60 <= trend < 85:
            votes["Transitional"] += 1

        # -------------------------
        # Disrupted
        # -------------------------

        if demand < 60:
            votes["Disrupted"] += 1

        if economic < 70:
            votes["Disrupted"] += 1

        if trend < 60:
            votes["Disrupted"] += 1

        regime = max(votes, key=votes.get)

        # ==========================================================
        # Better Confidence Calculation
        # ==========================================================

        if regime == "Stable":

            confidence = round(
                (demand + economic + trend) / 3,
                2
            )

        elif regime == "Seasonal":

            confidence = round(
                (seasonality + demand + trend) / 3,
                2
            )

        elif regime == "Transitional":

            confidence = round(
                (demand + trend + economic) / 3,
                2
            )

        else:

            confidence = round(
                100 - scsi,
                2
            )

        confidence = max(50, min(confidence, 99))

        # ==========================================================
        # Initial Fusion Strategy
        # ==========================================================

        fusion_weights = {

            "Stable": {
                "Prophet": 0.70,
                "XGBoost": 0.20,
                "LSTM": 0.10
            },

            "Seasonal": {
                "Prophet": 0.50,
                "XGBoost": 0.20,
                "LSTM": 0.30
            },

            "Transitional": {
                "Prophet": 0.35,
                "XGBoost": 0.35,
                "LSTM": 0.30
            },

            "Disrupted": {
                "Prophet": 0.15,
                "XGBoost": 0.60,
                "LSTM": 0.25
            }

        }

        descriptions = {

            "Stable":
            "Stable market with consistent demand patterns.",

            "Seasonal":
            "Seasonal fluctuations detected.",

            "Transitional":
            "Market conditions are changing and require balanced forecasting.",

            "Disrupted":
            "High volatility detected. Supply chain requires close monitoring."

        }

        decision_summary = {

            "Stable": [

                "Demand volatility is minimal.",

                "Economic indicators remain stable.",

                "Historical trends are consistent.",

                "Prophet is expected to perform best."

            ],

            "Seasonal": [

                "Holiday effects are increasing.",

                "Seasonal demand patterns detected.",

                "LSTM contributes more strongly."

            ],

            "Transitional": [

                "Market conditions are evolving.",

                "Balanced ensemble recommended.",

                "Monitor trend changes closely."

            ],

            "Disrupted": [

                "Demand volatility is high.",

                "Economic instability detected.",

                "Feature-driven forecasting is prioritized."

            ]

        }

        return {

            "regime": regime,

            "confidence": confidence,

            "risk_level": self.get_risk_level(scsi),

            "recommended_strategy": descriptions[regime],

            "recommended_model": fusion_weights[regime],

            "decision_summary": decision_summary[regime],

            "votes": votes

        }
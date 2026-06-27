class FusionEngine:

    def __init__(self):

        self.regime_priors = {

            "Stable": {
                "Prophet": 0.50,
                "XGBoost": 0.25,
                "LSTM": 0.25
            },

            "Seasonal": {
                "Prophet": 0.40,
                "XGBoost": 0.20,
                "LSTM": 0.40
            },

            "Transitional": {
                "Prophet": 0.33,
                "XGBoost": 0.33,
                "LSTM": 0.34
            },

            "Disrupted": {
                "Prophet": 0.20,
                "XGBoost": 0.50,
                "LSTM": 0.30
            }

        }

    def normalize(self, weights):

        total = sum(weights.values())

        return {
            k: v / total
            for k, v in weights.items()
        }

    def combine(
        self,
        prophet_result,
        xgb_result,
        lstm_result,
        regime
    ):

        priors = self.regime_priors[regime]

        # -------------------------
        # Performance Scores
        # -------------------------

        prophet_perf = 1 / prophet_result["mae"]

        xgb_perf = 1 / xgb_result["mae"]

        lstm_perf = 1 / lstm_result["mae"]

        performance_scores = {

            "Prophet": prophet_perf,

            "XGBoost": xgb_perf,

            "LSTM": lstm_perf

        }

        performance_scores = self.normalize(
            performance_scores
        )

        # -------------------------
        # Adaptive Weights
        # -------------------------

        final_weights = {}

        for model in priors:

            final_weights[model] = (

                0.6 * priors[model]

                +

                0.4 * performance_scores[model]

            )

            final_weights = self.normalize(
                final_weights
            )

        # -------------------------
        # Final Forecast
        # -------------------------

        forecast = (

            prophet_result["prediction"]

            * final_weights["Prophet"]

            +

            xgb_result["prediction"]

            * final_weights["XGBoost"]

            +

            lstm_result["prediction"]

            * final_weights["LSTM"]

        )

        ensemble_confidence = (

            prophet_result["confidence"]

            * final_weights["Prophet"]

            +

            xgb_result["confidence"]

            * final_weights["XGBoost"]

            +

            lstm_result["confidence"]

            * final_weights["LSTM"]

        )

        return {

            "forecast": round(forecast, 2),

            "weights": {

                k: round(v * 100, 2)

                for k, v in final_weights.items()

            },

            "ensemble_confidence": round(
                ensemble_confidence,
                2
            )

        }
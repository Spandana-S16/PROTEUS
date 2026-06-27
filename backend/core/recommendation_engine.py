from backend.utils import confidence


class RecommendationEngine:

    def generate(self, stability, decision, fusion):

        scsi = stability["overall"]["score"]

        regime = decision["regime"]

        confidence = fusion["ensemble_confidence"]

        weights = fusion["weights"]

        inventory_score = 100 - scsi

        supplier_score = inventory_score

        forecast_score = 100 - confidence

        recommendations = []

    # ==========================================
    # Inventory Recommendation
    # ==========================================

        if inventory_score < 20:

            inventory_action = "Maintain current inventory levels."

            inventory_priority = "Low"

        elif inventory_score < 40:

            inventory_action = "Increase safety stock by approximately 10%."

            inventory_priority = "Medium"

        else:

            inventory_action = "Increase safety stock by approximately 20%."

            inventory_priority = "High"

        recommendations.append({

            "category": "Inventory",

            "priority": inventory_priority,

            "action": inventory_action

        })

    # ==========================================
    # Supplier Recommendation
    # ==========================================

        if regime == "Stable":

            supplier_action = "Continue existing supplier allocation."

        elif regime == "Seasonal":

            supplier_action = "Prepare additional supplier capacity for seasonal demand."

        elif regime == "Transitional":

            supplier_action = "Diversify suppliers to reduce operational risk."

        else:

            supplier_action = "Activate contingency suppliers immediately."

        recommendations.append({

            "category": "Suppliers",

            "priority": "Medium",

            "action": supplier_action

        })

    # ==========================================
    # Forecast Recommendation
    # ==========================================

        if confidence >= 85:

            forecast_action = "Forecast reliability is high. Weekly monitoring is sufficient."

        elif confidence >= 70:

            forecast_action = "Forecast reliability is moderate. Review forecasts every few days."

        else:

            forecast_action = "Forecast uncertainty is elevated. Review forecasts daily."

        recommendations.append({

            "category": "Forecast",

            "priority": "Low",

            "action": forecast_action

        })

    # ==========================================
    # AI Explanation
    # ==========================================

        explanation = (

            f"Market regime was classified as {regime}. "

            f"The overall Stability Score is {scsi:.2f}/100, "

            f"indicating {stability['overall']['status'].lower()} operating conditions. "

            f"The adaptive ensemble assigned "

            f"{weights['Prophet']:.2f}% weight to Prophet, "

            f"{weights['XGBoost']:.2f}% to XGBoost and "

            f"{weights['LSTM']:.2f}% to LSTM "

            f"based on current market characteristics and historical model performance. "

            f"The final ensemble confidence is {confidence:.2f}%."

        )

    # ==========================================
    # Executive Summary
    # ==========================================

        summary = {

            "Stable":
                "Supply chain conditions remain healthy with low demand volatility. Continue normal operations while monitoring for future regime shifts.",

            "Seasonal":
                "Seasonal demand patterns are expected. Plan inventory and procurement accordingly.",

            "Transitional":
                "Demand behaviour is changing. Increase monitoring and prepare adaptive inventory strategies.",

            "Disrupted":
                "Significant instability detected. Immediate mitigation strategies are recommended."

        }

        return {

            "inventory_risk": round(inventory_score,2),

            "supplier_risk": round(supplier_score,2),

            "forecast_uncertainty": round(forecast_score,2),

            "summary": summary[regime],

            "ai_explanation": explanation,

            "recommendations": recommendations

        }
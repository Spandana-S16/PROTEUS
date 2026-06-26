class RecommendationEngine:

    def generate(self, stability, decision, fusion):

        scsi = stability["overall"]["score"]

        regime = decision["regime"]

        confidence = fusion["ensemble_confidence"]

        recommendations = []

        inventory_score = 100 - scsi

        supplier_score = inventory_score

        forecast_score = 100 - confidence

        # ----------------------------------
        # Inventory
        # ----------------------------------

        if inventory_score < 20:

            recommendations.append({

                "category": "Inventory",

                "priority": "Low",

                "action": "Maintain current inventory levels."

            })

        elif inventory_score < 40:

            recommendations.append({

                "category": "Inventory",

                "priority": "Medium",

                "action": "Increase safety stock by 10%."

            })

        else:

            recommendations.append({

                "category": "Inventory",

                "priority": "High",

                "action": "Increase safety stock by 20%."

            })

        # ----------------------------------
        # Suppliers
        # ----------------------------------

        if regime == "Stable":

            supplier_action = "Maintain supplier allocation."

        elif regime == "Seasonal":

            supplier_action = "Prepare backup supplier capacity."

        elif regime == "Transitional":

            supplier_action = "Diversify suppliers."

        else:

            supplier_action = "Immediately activate contingency suppliers."

        recommendations.append({

            "category": "Suppliers",

            "priority": "Medium",

            "action": supplier_action

        })

        # ----------------------------------
        # Forecast Confidence
        # ----------------------------------

        if confidence > 90:

            forecast_action = "Forecast confidence is very high."

        elif confidence > 80:

            forecast_action = "Monitor demand weekly."

        else:

            forecast_action = "Review forecasts daily."

        recommendations.append({

            "category": "Forecast",

            "priority": "Low",

            "action": forecast_action

        })

        # ----------------------------------
        # Executive Summary
        # ----------------------------------

        summary = {

            "Stable":

                "Supply chain conditions are healthy. Continue normal operations.",

            "Seasonal":

                "Prepare for predictable seasonal demand fluctuations.",

            "Transitional":

                "Demand patterns are changing. Monitor closely.",

            "Disrupted":

                "Supply chain disruption detected. Immediate intervention recommended."

        }

        return {

            "inventory_risk": round(inventory_score,2),

            "supplier_risk": round(supplier_score,2),

            "forecast_uncertainty": round(forecast_score,2),

            "summary": summary[regime],

            "recommendations": recommendations

        }
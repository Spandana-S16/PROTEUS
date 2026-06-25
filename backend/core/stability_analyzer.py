from datetime import datetime


class StabilityAnalyzer:
    """
    PROTEUS Stability Analyzer

    Computes:
    - Demand Stability
    - Economic Stability
    - Trend Stability
    - Seasonality Stability
    - Overall Supply Chain Stability Index (SCSI)

    Also returns:
    - Human-readable status
    - Reasons
    - Diagnostics
    - Timestamp
    """

    def get_status(self, score):
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Moderate"
        else:
            return "Poor"

    def calculate_scores(self, df):

        df = df.copy()

        diagnostics = {}

        # =====================================================
        # DEMAND STABILITY
        # =====================================================

        demand_cv = df["Rolling_CV"].mean()

        demand_score = max(
            0,
            min(100, 100 * (1 - demand_cv))
        )

        diagnostics["Rolling_CV"] = round(demand_cv, 4)

        demand_reason = (
            "Demand variability remained consistently low."
            if demand_score >= 85
            else "Demand showed moderate fluctuations."
            if demand_score >= 70
            else "Demand volatility is increasing."
        )

        # =====================================================
        # ECONOMIC STABILITY
        # =====================================================

        fuel_change = df["Fuel_Change"].abs().mean()
        cpi_change = df["CPI_Change"].abs().mean()
        unemployment_change = df["Unemployment_Change"].abs().mean()

        economic_change = (
            fuel_change +
            cpi_change +
            unemployment_change
        )

        economic_score = max(
            0,
            min(100, 100 - economic_change * 40)
        )

        diagnostics["Fuel_Change"] = round(fuel_change, 4)
        diagnostics["CPI_Change"] = round(cpi_change, 4)
        diagnostics["Unemployment_Change"] = round(
            unemployment_change,
            4,
        )

        economic_reason = (
            "Macroeconomic indicators remained stable."
            if economic_score >= 85
            else "Economic indicators showed moderate variation."
            if economic_score >= 70
            else "Economic instability detected."
        )

        # =====================================================
        # TREND STABILITY
        # =====================================================

        growth_std = df["Demand_Growth"].std()

        trend_score = max(
            0,
            min(100, 100 * (1 - growth_std))
        )

        diagnostics["Demand_Growth_STD"] = round(
            growth_std,
            4,
        )

        trend_reason = (
            "Historical demand trend remained consistent."
            if trend_score >= 85
            else "Demand trend shows moderate changes."
            if trend_score >= 70
            else "Demand trend is highly unstable."
        )

        # =====================================================
        # SEASONALITY STABILITY
        # =====================================================

        holiday_ratio = df["Holiday_Flag"].mean()

        seasonality_score = max(
            0,
            min(100, 100 - holiday_ratio * 100)
        )

        diagnostics["Holiday_Ratio"] = round(
            holiday_ratio,
            4,
        )

        seasonality_reason = (
            "Minimal seasonal disruption detected."
            if seasonality_score >= 85
            else "Moderate seasonal effects observed."
            if seasonality_score >= 70
            else "High seasonal impact detected."
        )

        # =====================================================
        # OVERALL SCORE
        # =====================================================

        component_scores = [
            demand_score,
            economic_score,
            trend_score,
            seasonality_score,
        ]

        scsi = round(
            sum(component_scores) /
            len(component_scores),
            2,
        )

        # =====================================================
        # OUTPUT
        # =====================================================

        results = {

            "analysis_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "overall": {

                "score": scsi,

                "status": self.get_status(scsi)

            },

            "components": {

                "Demand Stability": {

                    "score": round(demand_score, 2),

                    "status": self.get_status(demand_score),

                    "reason": demand_reason

                },

                "Economic Stability": {

                    "score": round(economic_score, 2),

                    "status": self.get_status(economic_score),

                    "reason": economic_reason

                },

                "Trend Stability": {

                    "score": round(trend_score, 2),

                    "status": self.get_status(trend_score),

                    "reason": trend_reason

                },

                "Seasonality Stability": {

                    "score": round(seasonality_score, 2),

                    "status": self.get_status(seasonality_score),

                    "reason": seasonality_reason

                }

            },

            "diagnostics": diagnostics

        }

        return results
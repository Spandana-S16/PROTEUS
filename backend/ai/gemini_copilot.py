import google.generativeai as genai


class GeminiCopilot:

    def __init__(self, api_key):

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def explain(self, stability, decision, fusion, recommendation):

        prompt = f"""
            You are an AI Supply Chain Copilot.

            Analyze the following forecast results and generate an executive business report.

            Stability Score:
                {stability['overall']['score']}

            Market Status:
                {stability['overall']['status']}

            Market Regime:
                {decision['regime']}

            Risk Level:
                {decision['risk_level']}

            Forecast:
                {fusion['forecast']}

            Ensemble Confidence:
                {fusion['ensemble_confidence']}%

            Model Weights:
                {fusion['weights']}

            Summary:
                {recommendation['summary']}

            Recommendations:
                {recommendation['recommendations']}

                Generate a professional report with exactly these sections:

                1. Executive Summary

                2. Why the AI reached this decision

                3. Business Risks

                4. Recommended Actions

                5. Overall Outlook

                Keep the tone concise, executive-friendly and easy for supply chain managers to understand.
                    """

        response = self.model.generate_content(prompt)

        return response.text
import os
import json
import logging
import pandas as pd
from openai import AzureOpenAI

class IntelligenceEngine:
    def __init__(self):
        self.api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

        if self.api_key and self.endpoint:
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=self.endpoint
            )
        else:
            self.client = None
            logging.warning("Azure OpenAI credentials not found. Intelligence Engine running in mock mode.")

    def analyze_performance(self, data_df: pd.DataFrame, context: str = "", analysis_type: str = "anomaly") -> dict:
        """
        Analyzes a pandas DataFrame of marketing performance data using GPT-4o.

        Args:
            data_df (pd.DataFrame): The marketing data to analyze.
            context (str): Contextual info (e.g. Tenant ID, Date Range).
            analysis_type (str): 'anomaly', 'trend', or 'opportunity'.
        """
        if self.client is None:
            return self._mock_analysis(data_df, analysis_type)

        # 1. Serialize Data to Markdown Table (efficient for LLMs)
        # Limit rows to prevent context window overflow.
        # Ensure we send relevant columns.
        summary_df = data_df.head(50).to_markdown(index=False)

        # 2. Select System Prompt based on Analysis Type
        system_prompt = self._get_system_prompt(analysis_type)

        user_prompt = f"""Context: {context}

        Data:
        {summary_df}

        Analyze this data according to the system instructions."""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logging.error(f"Error during AI analysis: {str(e)}")
            return {"error": str(e), "insights": []}

    def _get_system_prompt(self, analysis_type: str) -> str:
        base_instruction = """You are a Senior Marketing Analyst. Return the output as a valid JSON object with a list of 'insights'.
        Each insight object must have:
        - 'title': A short, punchy headline.
        - 'severity': 'high', 'medium', or 'low'.
        - 'description': A detailed explanation of the finding.
        - 'action_item': A recommended step to take."""

        if analysis_type == 'trend':
            return base_instruction + """
            Focus on identifying long-term patterns:
            1. Directional shifts in key metrics (Spend, CPA, ROAS) over the data period.
            2. Correlation between spend increases and conversion volume.
            3. Seasonality or day-of-week performance differences if evident."""

        elif analysis_type == 'opportunity':
            return base_instruction + """
            Focus on optimization opportunities:
            1. Identify under-utilized budgets in high-performing campaigns.
            2. Recommend bid adjustments for keywords/ad groups with high ROAS.
            3. Suggest reallocating spend from poor performers to top performers."""

        else: # anomaly (default)
            return base_instruction + """
            Focus on critical anomalies and immediate risks:
            1. High Spend but Zero/Low Conversions (Wasted Spend).
            2. Sudden spikes in CPA (>20% day-over-day).
            3. Significant drops in CTR indicating ad fatigue.
            4. Budget pacing issues (spending too fast or too slow)."""

    def _mock_analysis(self, df, analysis_type):
        """Returns dummy insights if no API key is present."""
        logging.info(f"Generating mock {analysis_type} insights...")

        if analysis_type == 'trend':
            return {
                "insights": [
                    {
                        "title": "CPA Trending Down",
                        "severity": "low",
                        "description": "Cost Per Acquisition has decreased by 15% over the last 7 days, indicating improved campaign efficiency.",
                        "action_item": "Consider scaling budget on these efficient campaigns."
                    }
                ]
            }
        elif analysis_type == 'opportunity':
             return {
                "insights": [
                    {
                        "title": "Scale 'Retargeting' Campaign",
                        "severity": "medium",
                        "description": "The 'Retargeting' campaign has a ROAS of 4.5 but limited budget.",
                        "action_item": "Increase daily budget by 20% to capture more demand."
                    }
                ]
            }
        else:
            return {
                "insights": [
                    {
                        "title": "High CPA Alert",
                        "severity": "high",
                        "description": "Campaign 'Summer_Promo' has a CPA of $50, which is 25% higher than average.",
                        "action_item": "Pause low-performing ad sets within this campaign immediately."
                    }
                ]
            }

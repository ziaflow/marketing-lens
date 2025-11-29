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

    def analyze_performance(self, data_df: pd.DataFrame, context: str = "") -> dict:
        """
        Analyzes a pandas DataFrame of marketing performance data using GPT-4o.
        """
        if self.client is None:
            return self._mock_analysis(data_df)

        # 1. Serialize Data to Markdown Table (efficient for LLMs)
        # Limit rows to prevent context window overflow
        summary_df = data_df.head(50).to_markdown(index=False)

        # 2. Construct Prompt
        system_prompt = """You are a Senior Marketing Analyst. Your goal is to identify critical anomalies
        and opportunities in the provided campaign performance data.
        Focus on:
        1) High Spend but Low ROAS/Conversions.
        2) Sudden Spikes in CPA (>20%).
        3) High performing organic content.

        Return the output as a valid JSON object with a list of 'insights'.
        Each insight should have: 'title', 'severity' (high/medium/low), and 'description'."""

        user_prompt = f"""Context: {context}

        Data:
        {summary_df}

        Analyze this data."""

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

    def _mock_analysis(self, df):
        """Returns dummy insights if no API key is present."""
        logging.info("Generating mock insights...")
        return {
            "insights": [
                {
                    "title": "Mock Insight: High CPA",
                    "severity": "high",
                    "description": "Campaign 'Summer_Promo' has a CPA of $50, which is 25% higher than average."
                },
                {
                    "title": "Mock Insight: Good Engagement",
                    "severity": "low",
                    "description": "Organic posts on LinkedIn are seeing a 5% engagement rate lift."
                }
            ]
        }

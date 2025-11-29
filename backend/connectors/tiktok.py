import requests
import logging

class TikTokConnector:
    def __init__(self, access_token):
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"
        self.access_token = access_token
        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    def get_campaign_report(self, advertiser_id, start_date, end_date):
        """
        Fetches campaign performance report.
        Endpoint: /report/integrated/get/
        """
        url = f"{self.base_url}/report/integrated/get/"
        params = {
            "advertiser_id": advertiser_id,
            "report_type": "BASIC",
            "data_level": "AUCTION_CAMPAIGN",
            "dimensions": '["campaign_id", "stat_time_day"]',
            "metrics": '["campaign_name", "spend", "impressions", "clicks", "conversion", "total_purchase_value"]',
            "start_date": start_date, # YYYY-MM-DD
            "end_date": end_date,
            "page_size": 1000
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

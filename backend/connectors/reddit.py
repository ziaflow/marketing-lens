import requests
import logging

class RedditConnector:
    def __init__(self, access_token):
        self.base_url = "https://ads-api.reddit.com/api/v2.0"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_campaign_reporting(self, account_id, start_date, end_date):
        """
        Fetches reporting data.
        Endpoint: /scope/{account_id}/reporting/
        """
        url = f"{self.base_url}/scope/{account_id}/reporting/"
        params = {
            "starts_at": start_date, # ISO 8601
            "ends_at": end_date,
            "group_by": "campaign_id",
            "metrics": "impressions,clicks,spend,conversion"
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

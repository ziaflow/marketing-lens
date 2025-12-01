import requests
import logging

class LinkedInConnector:
    def __init__(self, access_token):
        self.base_url = "https://api.linkedin.com/v2"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def get_ad_analytics(self, ad_account_id, start_date, end_date):
        """
        Fetches ad analytics.
        Endpoint: /adAnalyticsV2
        """
        url = f"{self.base_url}/adAnalyticsV2"
        params = {
            "q": "analytics",
            "pivot": "CAMPAIGN",
            "dateRange.start.day": start_date.day,
            "dateRange.start.month": start_date.month,
            "dateRange.start.year": start_date.year,
            "dateRange.end.day": end_date.day,
            "dateRange.end.month": end_date.month,
            "dateRange.end.year": end_date.year,
            "timeGranularity": "DAILY",
            "accounts": f"urn:li:sponsoredAccount:{ad_account_id}"
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_company_page_stats(self, organization_urn):
        """
        Fetches organic page statistics.
        Endpoint: /organizationalEntityShareStatistics
        """
        url = f"{self.base_url}/organizationalEntityShareStatistics"
        params = {
            "q": "organizationalEntity",
            "organizationalEntity": organization_urn
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

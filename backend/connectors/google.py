import requests
import logging

class GoogleConnector:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_search_console_data(self, site_url, start_date, end_date):
        """
        Fetches GSC Search Analytics.
        Endpoint: https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
        """
        # URL encode site_url usually needed, assuming handled by caller or lib
        url = f"https://www.googleapis.com/webmasters/v3/sites/{site_url}/searchAnalytics/query"
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query", "page", "device"],
            "rowLimit": 5000
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_ga4_report(self, property_id, start_date, end_date):
        """
        Fetches GA4 Data.
        Endpoint: https://analyticsdata.googleapis.com/v1beta/properties/{propertyId}:runReport
        """
        url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
        payload = {
            "dateRanges": [{"startDate": start_date, "endDate": end_date}],
            "dimensions": [{"name": "eventName"}],
            "metrics": [
                {"name": "sessions"},
                {"name": "totalUsers"},
                {"name": "conversions"}
            ]
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

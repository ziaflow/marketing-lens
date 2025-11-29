import requests
import logging
import urllib.parse

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
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/searchAnalytics/query"
        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query", "page", "device"],
            "rowLimit": 5000
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_site_list(self):
        """
        Lists the user's Search Console sites.
        Endpoint: https://www.googleapis.com/webmasters/v3/sites
        """
        url = "https://www.googleapis.com/webmasters/v3/sites"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_sitemaps(self, site_url):
        """
        Lists sitemaps for a specific site.
        Endpoint: https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/sitemaps"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def inspect_url(self, site_url, inspection_url):
        """
        Inspects a specific URL using the Index Inspection API.
        Endpoint: https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
        """
        url = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
        payload = {
            "inspectionUrl": inspection_url,
            "siteUrl": site_url,
            "languageCode": "en-US"
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

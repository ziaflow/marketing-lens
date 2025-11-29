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

    # --- Search Analytics ---
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

    # --- Sites ---
    def get_site_list(self):
        """
        Lists the user's Search Console sites.
        Endpoint: GET /sites
        """
        url = "https://www.googleapis.com/webmasters/v3/sites"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_site(self, site_url):
        """
        Retrieves information about specific site.
        Endpoint: GET /sites/{siteUrl}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_site(self, site_url):
        """
        Adds a site to the set of the user's sites in Search Console.
        Endpoint: PUT /sites/{siteUrl}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.json() # Usually returns 204 No Content, but check docs

    def delete_site(self, site_url):
        """
        Removes a site from the set of the user's sites in Search Console.
        Endpoint: DELETE /sites/{siteUrl}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    # --- Sitemaps ---
    def get_sitemaps(self, site_url):
        """
        Lists sitemaps for a specific site.
        Endpoint: GET /sites/{siteUrl}/sitemaps
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/sitemaps"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_sitemap(self, site_url, feed_path):
        """
        Retrieves information about a specific sitemap.
        Endpoint: GET /sites/{siteUrl}/sitemaps/{feedpath}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        encoded_feed_path = urllib.parse.quote(feed_path, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/sitemaps/{encoded_feed_path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def submit_sitemap(self, site_url, feed_path):
        """
        Submits a sitemap for a site.
        Endpoint: PUT /sites/{siteUrl}/sitemaps/{feedpath}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        encoded_feed_path = urllib.parse.quote(feed_path, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/sitemaps/{encoded_feed_path}"
        response = requests.put(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def delete_sitemap(self, site_url, feed_path):
        """
        Deletes a sitemap from this site.
        Endpoint: DELETE /sites/{siteUrl}/sitemaps/{feedpath}
        """
        encoded_site_url = urllib.parse.quote(site_url, safe="")
        encoded_feed_path = urllib.parse.quote(feed_path, safe="")
        url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site_url}/sitemaps/{encoded_feed_path}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    # --- URL Inspection ---
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

    # --- Google Analytics ---
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

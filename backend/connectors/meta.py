import requests
import logging

class MetaConnector:
    def __init__(self, access_token):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = access_token

    def get_ads_insights(self, ad_account_id, date_preset='yesterday'):
        """
        Fetches insights from the Marketing API.
        Endpoint: /{ad_account_id}/insights
        """
        url = f"{self.base_url}/{ad_account_id}/insights"
        params = {
            'access_token': self.access_token,
            'level': 'campaign',
            'date_preset': date_preset,
            'fields': 'campaign_name,campaign_id,impressions,clicks,spend,conversions,action_values',
            'limit': 100
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_page_insights(self, page_id, date_preset='yesterday'):
        """
        Fetches organic page insights.
        Endpoint: /{page_id}/insights
        """
        url = f"{self.base_url}/{page_id}/insights"
        params = {
            'access_token': self.access_token,
            'metric': 'page_impressions,page_post_engagements,page_fans',
            'period': 'day',
            'date_preset': date_preset
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

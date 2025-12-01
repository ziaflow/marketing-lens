from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Dimension,
    Metric,
)
from google.analytics.admin import AnalyticsAdminServiceClient
from google.oauth2 import service_account
import json
import os

class GoogleAnalyticsTools:
    def __init__(self, credentials_json: str = None):
        """
        Initializes the clients.
        If credentials_json is provided (as a JSON string), it uses that.
        Otherwise, it falls back to Application Default Credentials (ADC).
        """
        if credentials_json:
            info = json.loads(credentials_json)
            creds = service_account.Credentials.from_service_account_info(info)
            self.data_client = BetaAnalyticsDataClient(credentials=creds)
            self.admin_client = AnalyticsAdminServiceClient(credentials=creds)
        else:
            # ADC fallback
            self.data_client = BetaAnalyticsDataClient()
            self.admin_client = AnalyticsAdminServiceClient()

    def list_account_summaries(self):
        """
        Lists account summaries (Accounts and Properties).
        """
        results = []
        # ListAccountSummaries returns a pager
        for summary in self.admin_client.list_account_summaries(parent=""):
            results.append({
                "name": summary.name,
                "account": summary.account,
                "display_name": summary.display_name,
                "property_summaries": [
                    {"property": p.property, "display_name": p.display_name}
                    for p in summary.property_summaries
                ]
            })
        return results

    def run_report(self, property_id, start_date="7daysAgo", end_date="yesterday", dimensions=None, metrics=None):
        """
        Runs a basic report.
        """
        if dimensions is None:
            dimensions = ["date"]
        if metrics is None:
            metrics = ["activeUsers", "screenPageViews"]

        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )

        response = self.data_client.run_report(request)

        data = []
        for row in response.rows:
            item = {}
            for i, dim_val in enumerate(row.dimension_values):
                item[dimensions[i]] = dim_val.value
            for i, metric_val in enumerate(row.metric_values):
                item[metrics[i]] = metric_val.value
            data.append(item)
        return data

    def run_realtime_report(self, property_id, dimensions=None, metrics=None):
        """
        Runs a realtime report.
        """
        if dimensions is None:
            dimensions = ["country"]
        if metrics is None:
            metrics = ["activeUsers"]

        request = RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
        )

        response = self.data_client.run_realtime_report(request)

        data = []
        for row in response.rows:
            item = {}
            for i, dim_val in enumerate(row.dimension_values):
                item[dimensions[i]] = dim_val.value
            for i, metric_val in enumerate(row.metric_values):
                item[metrics[i]] = metric_val.value
            data.append(item)
        return data

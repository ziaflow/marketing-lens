import logging
import datetime
import time
import random
import os
import json
import requests
import pandas as pd
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

# Import Connectors
from connectors.meta import MetaConnector
from connectors.tiktok import TikTokConnector
from connectors.google import GoogleConnector
from connectors.linkedin import LinkedInConnector
from connectors.reddit import RedditConnector
from connectors.microsoft import MicrosoftAdsConnector

# Import Intelligence
from intelligence import IntelligenceEngine

# Import MCP
from mcp.server import GoogleAnalyticsMCPServer

app = func.FunctionApp()

# --- Helper Functions ---

def get_secret(secret_name):
    """Retrieves a secret from Azure Key Vault."""
    key_vault_name = os.environ.get("KEY_VAULT_NAME")
    if not key_vault_name:
        return "mock-secret-value"

    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    try:
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except ResourceNotFoundError:
        logging.error(f"Secret {secret_name} not found.")
        return None

# --- Ingestion Functions ---

@app.function_name(name="Fn_Ingest_Platform_Data")
@app.route(route="ingest", auth_level=func.AuthLevel.FUNCTION)
def ingest_platform_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tenant_id = req.params.get('tenant_id')
    platform_id = req.params.get('platform_id')

    if not tenant_id or not platform_id:
        return func.HttpResponse(
            "Please pass a tenant_id and platform_id on the query string",
            status_code=400
        )

    # Retrieve Token (Mock logic for retrieval key)
    token = get_secret(f"{tenant_id}-{platform_id}-token")
    if not token:
        # For demo purposes, if no secret, we might use a dummy token to allow the code to run 'dry'
        token = "dummy_token"

    try:
        if platform_id == 'GoogleSearchConsole':
            connector = GoogleConnector(token)

            # 1. Discover Sites (New functionality)
            sites = connector.get_site_list()
            site_count = len(sites.get('siteEntry', []))

            # 2. Process specific site (In real app, loop through all)
            # We use the previous example logic but now with proper encoding handling in the connector
            target_site = "https://example.com"
            data = connector.get_search_console_data(target_site, "2023-10-01", "2023-10-02")

            return func.HttpResponse(f"GSC Discovery: Found {site_count} sites. Ingested {len(data.get('rows', []))} rows for {target_site}.")

        elif platform_id == 'GoogleAnalytics':
            # Use MCP Implementation for GA4
            # Note: MCP implementation typically expects Service Account credentials.
            # In this context, we'll assume 'token' might be a JSON service account string or similar.
            # If not, it falls back to ADC as per the implementation.
            mcp_server = GoogleAnalyticsMCPServer(credentials_json=None)

            # Execute MCP Tool
            data = mcp_server.execute_tool("run_report", {
                "property_id": "123456",
                "start_date": "2023-10-01",
                "end_date": "2023-10-02",
                "metrics": ["sessions", "totalUsers", "conversions"]
            })

            # Handle potential error from MCP
            if isinstance(data, dict) and "error" in data:
                 return func.HttpResponse(f"GA4 MCP Error: {data['error']}", status_code=500)

            return func.HttpResponse(f"GA4 MCP Data Ingested: {len(data)} rows")

        elif platform_id == 'LinkedIn':
            connector = LinkedInConnector(token)
            # Fetch Ads
            ads_data = connector.get_ad_analytics("123456789", datetime.date(2023, 10, 1), datetime.date(2023, 10, 2))
            # Fetch Organic
            org_data = connector.get_company_page_stats("urn:li:organization:12345")
            return func.HttpResponse(f"LinkedIn Data Ingested")

        elif platform_id == 'Meta':
            connector = MetaConnector(token)
            data = connector.get_ads_insights("act_123456789")
            return func.HttpResponse(f"Meta Data Ingested")

        elif platform_id == 'TikTok':
            connector = TikTokConnector(token)
            data = connector.get_campaign_report("adv_12345", "2023-10-01", "2023-10-02")
            return func.HttpResponse(f"TikTok Data Ingested")

        elif platform_id == 'Reddit':
            connector = RedditConnector(token)
            data = connector.get_campaign_reporting("t2_12345", "2023-10-01", "2023-10-02")
            return func.HttpResponse(f"Reddit Data Ingested")

        elif platform_id == 'MicrosoftAds':
            connector = MicrosoftAdsConnector(token, "dev_token_123", "cust_123")
            data = connector.get_campaign_performance("12345", "Last7Days")
            return func.HttpResponse(f"Microsoft Ads Report Requested")

        else:
             return func.HttpResponse(f"Unknown Platform: {platform_id}", status_code=400)

    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        # In production, we return 500, but for 'dry run' demo we might want to return 200 with error message
        return func.HttpResponse(f"Ingestion Error (likely auth): {str(e)}", status_code=500)

# --- Intelligence Functions ---

@app.function_name(name="Fn_Generate_Insights")
@app.route(route="insights", auth_level=func.AuthLevel.FUNCTION)
def generate_insights(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generating AI Insights...')

    tenant_id = req.params.get('tenant_id')

    # 1. Fetch recent data from DB (Mocked here as DataFrame)
    # In real world: engine = create_engine(...); df = pd.read_sql(...)
    data = {
        'campaign_name': ['Campaign A', 'Campaign B', 'Campaign C'],
        'spend': [1200, 5000, 300],
        'impressions': [50000, 200000, 10000],
        'conversions': [40, 10, 15],
        'cpa': [30.0, 500.0, 20.0] # High CPA for B
    }
    df = pd.DataFrame(data)

    # 2. Initialize Intelligence Engine
    engine = IntelligenceEngine()

    # 3. Analyze
    insights = engine.analyze_performance(df, context=f"Tenant: {tenant_id}")

    # 4. Return or Store
    return func.HttpResponse(json.dumps(insights), mimetype="application/json")

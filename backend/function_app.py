import logging
import datetime
import time
import random
import os
import json
import requests
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

app = func.FunctionApp()

# 3.2.1 The OAuth Token Rotation Pattern
def get_secret(secret_name):
    """Retrieves a secret from Azure Key Vault."""
    key_vault_name = os.environ.get("KEY_VAULT_NAME")
    if not key_vault_name:
        return "mock-secret-value" # For local dev without env var

    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    try:
        retrieved_secret = client.get_secret(secret_name)
        return retrieved_secret.value
    except ResourceNotFoundError:
        logging.error(f"Secret {secret_name} not found.")
        return None

def update_secret(secret_name, new_value):
    """Updates a secret in Azure Key Vault (Atomic Update)."""
    key_vault_name = os.environ.get("KEY_VAULT_NAME")
    if not key_vault_name:
        logging.info(f"Mock Update Secret: {secret_name}")
        return

    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    client.set_secret(secret_name, new_value)
    logging.info(f"Secret {secret_name} updated successfully.")

# 3.2.2 Rate Limiting and Pagination strategy
def make_request_with_backoff(url, params=None, headers=None, max_retries=5):
    """Makes a request with Exponential Backoff and Jitter."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 429:
                # Too Many Requests
                wait_time = (2 ** attempt) + random.uniform(0, 1) # Backoff + Jitter
                logging.warning(f"Rate limited. Waiting {wait_time:.2f}s...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)

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

    # Dispatcher Logic based on Platform ID
    if platform_id == 'GoogleSearchConsole':
        return ingest_gsc(tenant_id)
    elif platform_id == 'GoogleAnalytics':
        return ingest_ga4(tenant_id)
    elif platform_id == 'LinkedIn':
        return ingest_linkedin(tenant_id)
    elif platform_id in ['Meta', 'TikTok', 'Google']:
        return ingest_paid_media(tenant_id, platform_id)
    else:
         return func.HttpResponse(f"Unknown Platform: {platform_id}", status_code=400)

def ingest_paid_media(tenant_id, platform):
    logging.info(f"Starting Paid Media Ingestion for {platform} - {tenant_id}")
    # Mock Ingestion Logic simulating API response
    data = [
        {"date": "2023-10-27", "campaign_name": "Summer_Promo", "impressions": 1000, "spend": 50.00},
        {"date": "2023-10-27", "campaign_name": "Retargeting", "impressions": 500, "spend": 25.00}
    ]
    # In real app: Write to Blob Storage (Bronze Layer)
    logging.info(f"Ingested {len(data)} records for {platform}")
    return func.HttpResponse(f"Ingested {len(data)} records for {tenant_id} on {platform}", status_code=200)

def ingest_gsc(tenant_id):
    logging.info(f"Starting GSC Ingestion for {tenant_id}")
    # Logic to fetch Search Analytics API
    # Mocking Google Search Console API Response
    # https://developers.google.com/webmaster-tools/v1/searchanalytics/query
    mock_response = {
        "rows": [
            {"keys": ["marketing analytics"], "clicks": 150, "impressions": 2000, "ctr": 0.075, "position": 4.5},
            {"keys": ["marketing dashboard"], "clicks": 80, "impressions": 1200, "ctr": 0.066, "position": 6.2}
        ]
    }

    # Simulate processing
    processed_count = 0
    for row in mock_response["rows"]:
        # Extract metrics
        keyword = row["keys"][0]
        clicks = row["clicks"]
        # In real app: Transform to schema and Load to DB
        processed_count += 1

    logging.info(f"Processed {processed_count} GSC keywords.")
    return func.HttpResponse(f"GSC Ingestion: Processed {processed_count} keywords for {tenant_id}")

def ingest_ga4(tenant_id):
    logging.info(f"Starting GA4 Ingestion for {tenant_id}")
    # Logic to fetch GA4 Data API
    # Mocking GA4 RunReport Response
    mock_response = {
        "rows": [
            {"dimensionValues": [{"value": "20231027"}], "metricValues": [{"value": "45200"}, {"value": "1.2"}]} # Sessions, Engagement Rate
        ]
    }

    processed_count = len(mock_response["rows"])
    return func.HttpResponse(f"GA4 Ingestion: Processed {processed_count} daily records for {tenant_id}")

def ingest_linkedin(tenant_id):
    logging.info(f"Starting LinkedIn Ingestion for {tenant_id}")
    # Logic to fetch LinkedIn Marketing Developer Platform API

    # 1. Company Page Statistics Mock
    mock_page_stats = {
        "followers_total": 8540,
        "new_followers": 150,
        "page_views": 320,
        "unique_visitors": 210
    }

    # 2. Ad Analytics Mock
    mock_ad_stats = [
        {"campaign_id": "urn:li:sponsoredCampaign:123", "impressions": 5000, "spend": 120.50}
    ]

    logging.info(f"Ingested LinkedIn Page Stats and {len(mock_ad_stats)} Ad Campaign records.")
    return func.HttpResponse(f"LinkedIn Ingestion: Success for {tenant_id}")

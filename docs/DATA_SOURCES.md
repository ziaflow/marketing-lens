# Data Source Integration Guide

This document outlines the configuration and API details for the supported marketing platforms in Marketing Lens.

## 1. Meta (Facebook & Instagram)
**Type:** Paid Media & Organic Social
- **API:** [Graph API v18.0](https://developers.facebook.com/docs/graph-api/)
- **Endpoints Used:**
    - `/{ad_account_id}/insights`: For campaign performance (Impressions, Spend, Clicks).
    - `/{page_id}/insights`: For organic page reach and engagement.
- **Auth:** OAuth 2.0 (User Access Token or System User Token).
- **Scopes:** `ads_read`, `pages_read_engagement`, `read_insights`.
- **Data Mapping:**
    - `spend` -> `fact_performance_daily.spend`
    - `impressions` -> `fact_performance_daily.impressions`

## 2. TikTok
**Type:** Paid Media
- **API:** [TikTok Marketing API v1.3](https://ads.tiktok.com/marketing_api/docs)
- **Endpoints Used:**
    - `/report/integrated/get/`: Synchronous reporting endpoint for campaign stats.
- **Auth:** OAuth 2.0 (Access Token in Header).
- **Scopes:** `ads_read`.
- **Data Mapping:**
    - `total_purchase_value` -> `fact_performance_daily.conversion_value`

## 3. Google Ads / Analytics / Search Console
**Type:** Multi-channel
- **APIs:**
    - **Search Console:**
        - `webmasters.searchanalytics.query` for SEO (Clicks, Position).
        - `webmasters.sites.list` for property discovery.
        - `webmasters.sitemaps.list` for sitemap monitoring.
        - `urlInspection.index.inspect` for detailed URL indexing status.
    - **GA4:** `properties.runReport` for Web Analytics (Sessions, Conversions).
- **Auth:** Google OAuth 2.0 / Service Account.
- **Scopes:**
    - `https://www.googleapis.com/auth/webmasters.readonly`
    - `https://www.googleapis.com/auth/analytics.readonly`

## 4. LinkedIn
**Type:** B2B Paid & Organic
- **API:** [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- **Endpoints Used:**
    - `/adAnalyticsV2`: For sponsored campaign daily metrics.
    - `/organizationalEntityShareStatistics`: For Company Page stats.
- **Auth:** OAuth 2.0 (3-legged).
- **Scopes:** `r_ads_reporting`, `r_organization_social`.

## 5. Reddit
**Type:** Paid Media
- **API:** [Reddit Ads API v2.0](https://ads-api.reddit.com/docs/)
- **Endpoints Used:**
    - `/scope/{account_id}/reporting/`: For granular campaign reporting.
- **Auth:** OAuth 2.0 (Bearer Token).
- **Scopes:** `ads_read`.

## 6. Microsoft Ads (Bing)
**Type:** Paid Search
- **API:** [Microsoft Advertising API (Bing Ads)](https://learn.microsoft.com/en-us/advertising/guides/get-started)
- **Integration:**
    - Uses the `CampaignManagementService` (SOAP/JSON).
    - **Note:** Reporting is asynchronous. Request Report -> Poll -> Download.
- **Auth:** OAuth 2.0 + Developer Token + Customer ID.
- **Scopes:** `msads.manage`.

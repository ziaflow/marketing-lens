-- Unified Marketing Schema (UMS)
-- Section 4.1.1 of Architectural Blueprint + Extensions for GSC, GA4, LinkedIn

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Dimension: Campaigns
CREATE TABLE dim_campaign (
    campaign_key BIGSERIAL PRIMARY KEY,
    platform_campaign_id TEXT NOT NULL,
    campaign_name TEXT,
    platform_source TEXT CHECK (platform_source IN ('Meta', 'TikTok', 'Google', 'GoogleAnalytics', 'GoogleSearchConsole', 'LinkedIn', 'Reddit', 'MicrosoftAds')),
    objective TEXT,
    metadata JSONB
);

-- Dimension: Ad Groups
CREATE TABLE dim_adgroup (
    adgroup_key BIGSERIAL PRIMARY KEY,
    platform_adgroup_id TEXT NOT NULL,
    adgroup_name TEXT,
    metadata JSONB
);

-- Dimension: Ads
CREATE TABLE dim_ad (
    ad_key BIGSERIAL PRIMARY KEY,
    platform_ad_id TEXT NOT NULL,
    ad_name TEXT,
    metadata JSONB
);

-- Dimension: Keywords (for Google Search Console)
CREATE TABLE dim_keyword (
    keyword_key BIGSERIAL PRIMARY KEY,
    keyword_text TEXT NOT NULL,
    metadata JSONB
);

-- Dimension: Pages (for Organic/Company Page Info)
CREATE TABLE dim_page (
    page_key BIGSERIAL PRIMARY KEY,
    platform_page_id TEXT NOT NULL, -- e.g., LinkedIn Company ID, FB Page ID
    page_name TEXT,
    platform_source TEXT CHECK (platform_source IN ('Meta', 'LinkedIn', 'TikTok', 'Reddit')),
    metadata JSONB
);

-- Fact Table: Daily Performance (Paid Media)
CREATE TABLE fact_performance_daily (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    date DATE NOT NULL,
    campaign_key BIGINT REFERENCES dim_campaign(campaign_key),
    adgroup_key BIGINT REFERENCES dim_adgroup(adgroup_key),
    ad_key BIGINT REFERENCES dim_ad(ad_key),
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    spend DECIMAL(19,4) DEFAULT 0.0000,
    conversions BIGINT DEFAULT 0,
    conversion_value DECIMAL(19,4) DEFAULT 0.0000,
    custom_metrics JSONB
);

-- Fact Table: Daily Search Performance (GSC)
CREATE TABLE fact_search_daily (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    date DATE NOT NULL,
    keyword_key BIGINT REFERENCES dim_keyword(keyword_key),
    page_url TEXT, -- Can be a dimension if URL cardinality is low, usually text is fine for GSC
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    position DECIMAL(10,2), -- Average Position
    ctr DECIMAL(10,4), -- Click Through Rate
    custom_metrics JSONB
);

-- Fact Table: Daily Organic/Page Performance (LinkedIn, Meta Page, TikTok Profile)
CREATE TABLE fact_organic_daily (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    date DATE NOT NULL,
    page_key BIGINT REFERENCES dim_page(page_key),
    followers_total BIGINT DEFAULT 0,
    followers_gained BIGINT DEFAULT 0,
    page_views BIGINT DEFAULT 0,
    engagement_rate DECIMAL(10,4),
    custom_metrics JSONB -- To store platform specific things like "Interactive Sticker Taps" or "LinkedIn Unique Visitors"
);

-- Intelligence Layer: Insights Storage
CREATE TABLE insights (
    insight_id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL,
    insight_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    type TEXT, -- 'anomaly', 'trend', 'opportunity'
    severity TEXT, -- 'high', 'medium', 'low'
    title TEXT,
    message TEXT,
    action_item TEXT,
    data_context JSONB -- Stores the specific row/data that triggered the insight
);

-- Indexes
CREATE INDEX idx_fact_perf_tenant_date ON fact_performance_daily (tenant_id, date);
CREATE INDEX idx_fact_search_tenant_date ON fact_search_daily (tenant_id, date);
CREATE INDEX idx_fact_organic_tenant_date ON fact_organic_daily (tenant_id, date);
CREATE INDEX idx_insights_tenant_date ON insights (tenant_id, insight_date);

CREATE INDEX idx_fact_perf_campaign ON fact_performance_daily (campaign_key);
CREATE INDEX idx_dim_campaign_platform_id ON dim_campaign (platform_campaign_id);

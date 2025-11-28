-- Enable UUID extension for tenant isolation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Schema: config
-- Stores tenant configuration and platform enablement
CREATE SCHEMA IF NOT EXISTS config;

CREATE TABLE config.active_tenants (
    tenant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    subdomain TEXT NOT NULL UNIQUE, -- Used for Middleware resolution
    platforms JSONB NOT NULL DEFAULT '[]', -- e.g. ["META", "TIKTOK"]
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Schema: public (Data Warehouse)
-- Star Schema Implementation

-- Dimension: Campaigns
CREATE TABLE dim_campaign (
    campaign_key BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES config.active_tenants(tenant_id),
    platform_campaign_id TEXT NOT NULL,
    platform_source TEXT NOT NULL CHECK (platform_source IN ('META', 'TIKTOK', 'GOOGLE')),
    campaign_name TEXT,
    objective TEXT,
    metadata JSONB, -- Stores platform-specific attributes
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, platform_source, platform_campaign_id)
);

-- Fact: Daily Performance
CREATE TABLE fact_performance_daily (
    id BIGSERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES config.active_tenants(tenant_id),
    date DATE NOT NULL,
    campaign_key BIGINT NOT NULL REFERENCES dim_campaign(campaign_key),
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    spend DECIMAL(19,4) DEFAULT 0.0000,
    conversions BIGINT DEFAULT 0,
    conversion_value DECIMAL(19,4) DEFAULT 0.0000,
    custom_metrics JSONB, -- Handles schema drift (e.g., "tiktok_likes")
    currency_code CHAR(3) DEFAULT 'USD',
    UNIQUE(tenant_id, date, campaign_key)
);

-- Indexing for Performance
CREATE INDEX idx_fact_date ON fact_performance_daily(date);
CREATE INDEX idx_fact_tenant_date ON fact_performance_daily(tenant_id, date);
CREATE INDEX idx_dim_campaign_platform ON dim_campaign(platform_source, platform_campaign_id);

-- ----------------------------------------------------------------------
-- FUTURE FEATURE: Customer Portal Invoicing
-- ----------------------------------------------------------------------

CREATE TABLE invoices (
    invoice_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL REFERENCES config.active_tenants(tenant_id),
    invoice_number TEXT NOT NULL,
    billing_period_start DATE NOT NULL,
    billing_period_end DATE NOT NULL,
    total_amount DECIMAL(19,2) NOT NULL,
    currency CHAR(3) DEFAULT 'USD',
    status TEXT CHECK (status IN ('PAID', 'PENDING', 'OVERDUE')),
    file_url TEXT, -- Path to Blob Storage PDF
    email_sent_at TIMESTAMPTZ, -- Tracks when the user requested an email
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_invoices_tenant ON invoices(tenant_id);

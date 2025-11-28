# Database Schema: PostgreSQL Star Schema

This directory contains the SQL scripts to initialize the **Unified Marketing Schema (UMS)** on Azure Database for PostgreSQL Flexible Server.

## Files

- `schema.sql`: The DDL definitions for tables, indexes, and constraints.

## Schema Overview

- **Dimensions**: `dim_campaign`, `dim_adgroup`, etc.
- **Facts**: `fact_performance_daily`.
- **Config**: `config.active_tenants`.
- **Invoices**: `invoices` (Placeholder for future portal features).

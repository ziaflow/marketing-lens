# Backend Architecture: Azure Functions

This directory contains the Python-based Azure Functions responsible for:

1.  **Data Ingestion**: Fetching data from external APIs (Meta, TikTok, Google).
2.  **Token Management**: Rotating OAuth tokens via Azure Key Vault.
3.  **Intelligence**: Generating insights using Azure OpenAI (GPT-4o).

## Directory Structure

- `functions/`: Individual function code.
- `shared/`: Shared libraries for database connections and API wrappers.
- `requirements.txt`: Python dependencies.

## Key Functions

- `Fn_Ingest_Platform_Data`: Triggered by Azure Data Factory.
- `Fn_Generate_Insights`: Triggered after daily transformation.

import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tenant_id = req.params.get('tenant_id')
    if not tenant_id:
        return func.HttpResponse(
            "Please pass a tenant_id on the query string",
            status_code=400
        )

    # MOCK DATA - In production, this would query the PostgreSQL Star Schema
    # SELECT ... FROM fact_performance_daily WHERE tenant_id = ...

    mock_response = {
        "tenant_id": tenant_id,
        "summary": {
            "total_spend": 12450.00,
            "total_conversions": 842,
            "currency": "USD"
        },
        "chart_data": [
            { "date": "Mon", "spend": 1200, "conversions": 45 },
            { "date": "Tue", "spend": 1500, "conversions": 52 },
            { "date": "Wed", "spend": 1100, "conversions": 38 },
            { "date": "Thu", "spend": 1700, "conversions": 65 },
            { "date": "Fri", "spend": 2100, "conversions": 89 },
            { "date": "Sat", "spend": 2400, "conversions": 110 },
            { "date": "Sun", "spend": 1900, "conversions": 75 }
        ],
        "campaigns": [
            { "id": 1, "name": "Summer Sale 2024", "platform": "Meta", "status": "Active", "spend": 4500.00, "conversions": 120, "roas": 3.2 },
            { "id": 2, "name": "Brand Awareness", "platform": "TikTok", "status": "Active", "spend": 2100.50, "conversions": 45, "roas": 1.8 }
        ]
    }

    return func.HttpResponse(
        json.dumps(mock_response),
        mimetype="application/json",
        status_code=200
    )

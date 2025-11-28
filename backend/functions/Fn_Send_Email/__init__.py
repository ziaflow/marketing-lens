import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        invoice_id = req_body.get('invoice_id')
        tenant_id = req_body.get('tenant_id')
        recipient_email = req_body.get('email')

        if not invoice_id or not recipient_email:
            return func.HttpResponse(
                "Please pass invoice_id and email in the request body",
                status_code=400
            )

        # MOCK LOGIC: In production, this would use SendGrid or Azure Communication Services
        logging.info(f"Sending Invoice {invoice_id} to {recipient_email} for Tenant {tenant_id}")

        # Simulating a successful email send
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "message": f"Invoice {invoice_id} sent to {recipient_email}"
            }),
            mimetype="application/json",
            status_code=200
        )

    except ValueError:
        return func.HttpResponse(
            "Invalid JSON",
            status_code=400
        )

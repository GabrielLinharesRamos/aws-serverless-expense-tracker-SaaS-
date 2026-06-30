import json
import uuid
from datetime import datetime
import logging

from expenses_repository import update_expense_repository
from shared.validators.allowed_fields_validator import validate_fields
from shared.validators.amount_validator import validate_amount

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def update_expense(event):

    expense_id = None

    try:

        expense_id = event["pathParameters"]["expense_id"]

        body = json.loads(event["body"])

        amount = body["amount"]
        description = body["description"]

        allowed_fields = {"amount", "description"}

        validate_fields(body,allowed_fields)

        amount = validate_amount(amount)

        family_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["custom:family_id"]

        update_expense_repository(family_id, expense_id, amount, description)

        logger.info(
            json.dumps(
                {
                    "message": "expense updated",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": "update_expense",
                    "status": "success"
                }
            )
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('expense updated')
        }

    except ValueError as e:

        logger.warning(
            json.dumps(
                {
                    "message": "Validation failed",
                    "expense_id": expense_id,
                    "error": str(e)
                }
            )
        )

        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": str(e)
                }
            )
        }
    
    except Exception as e:
        logger.exception(
            json.dumps(
                {
                    "message": "Failed to update the expense",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": 'update_expense',
                    "status": "failed",
                    "error": str(e)
                }
            )
        )

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }
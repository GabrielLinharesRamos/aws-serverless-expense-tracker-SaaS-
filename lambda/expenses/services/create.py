import json
import uuid
from datetime import datetime
import logging

from expenses_repository import save
from shared.validators.allowed_fields_validator import validate_fields
from shared.validators.amount_validator import validate_amount

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_expense(event):

    expense_id = None

    try:

        expense_id = str(uuid.uuid4())
        body = json.loads(event["body"])

        allowed_fields = {"amount", "description"}

        validate_fields(body,allowed_fields)

        amount = validate_amount(body["amount"])

        user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]

        expense = {
            'PK':f"USER#{user_id}",
            'SK':f"EXPENSE#{expense_id}",
            'entity_type': "EXPENSE",
            'amount': amount,
            'description': body["description"],
            'created_at': datetime.utcnow().isoformat()
        }

        save(expense)

        logger.info(
            json.dumps(
                {
                    "message": "expense created",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": "create_expense",
                    "status": "success"
                }
            )
        )
        
        return {
            'statusCode': 201,
            'body': json.dumps('expense Created')
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
        logger.error(
            json.dumps(
                {
                    "message": "Failed creating expense",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": 'create_expense',
                    "status": "failed",
                    "error": str(e)
                }
            )
        )

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e)
            })
        }
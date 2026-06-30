import json
import uuid
from datetime import datetime
import logging

from expenses_repository import exclude_expense_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def exclude_expense(event):

    expense_id = None

    try:

        expense_id = event["pathParameters"]["expense_id"]

        family_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["custom:family_id"]

        exclude_expense_repository(family_id, expense_id)

        logger.info(
            json.dumps(
                {
                    "message": "expense excluded",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": "exclude_expense",
                    "status": "success"
                }
            )
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('expense excluded')
        }
    
    except Exception as e:
        logger.exception(
            json.dumps(
                {
                    "message": "Failed to exclude expenses",
                    "request_id": event["requestContext"]["requestId"],
                    "expense_id": expense_id,
                    "event_type": 'exclude_expense',
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
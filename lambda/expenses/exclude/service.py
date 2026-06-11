import json
import uuid
from datetime import datetime
import logging

from shared.repositories.expense_repository import exclude_expense_repository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def exclude_expense(event):

    try:

        expense_id = event["pathParameters"]["expense_id"]

        exclude_expense_repository("ANONYMOUS", expense_id)
        
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
                    "event_type": 'exclude_expense',
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
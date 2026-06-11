import json
import uuid
from datetime import datetime
import logging

from shared.repositories.expense_repository import list_by_user

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def list_expense(event):

    try:

        expenses_list = list_by_user("USER#ANONYMOUS")
        
        return {
            'statusCode': 200,
            'body': json.dumps(expenses_list)
        }
    
    except Exception as e:
        logger.exception(
            json.dumps(
                {
                    "message": "Failed to list expenses",
                    "request_id": event["requestContext"]["requestId"],
                    "event_type": 'list_expense',
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
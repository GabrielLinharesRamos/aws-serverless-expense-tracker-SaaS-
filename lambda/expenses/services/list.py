import json
import uuid
import logging
from decimal import Decimal

from expenses_repository import list_by_user

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def list_expense(event):

    try:

        expenses_list = list_by_user("ANONYMOUS")
        
        return {
            'statusCode': 200,
            'body': expenses_list
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
                "message": str(e)
            })
        }
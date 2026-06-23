import json
import uuid
import logging
from decimal import Decimal

from expenses_repository import list_by_user

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def list_expense(event):

    try:

        user_id = event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
        expenses_list = list_by_user(user_id)
        
        
        return {
            'statusCode': 200,
            'body': json.dumps(expenses_list,default=lambda x: float(x) if isinstance(x, Decimal) else x),
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
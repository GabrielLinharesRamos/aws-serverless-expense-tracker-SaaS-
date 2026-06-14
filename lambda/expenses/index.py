from services.create import create_expense
from services.exclude import exclude_expense
from services.list import list_expense
from services.update import update_expense

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]

    if method == "POST":
        return create_expense(event)

    elif method == "GET":
        return list_expense(event)

    elif method == "PUT":
        return update_expense(event)

    elif method == "DELETE":
        return exclude_expense(event)

    return {
        "statusCode": 405,
        "body": "Method Not Allowed"
    }
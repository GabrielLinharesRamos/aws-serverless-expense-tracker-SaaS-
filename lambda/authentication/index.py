from services.login import login
from services.signup import signup

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]

    if method == "POST" and path == "/auth/signup":
        return signup(event)

    elif method == "POST" and path == "/auth/login":
        return login(event)

    return {
        "statusCode": 405,
        "body": "Method Not Allowed"
    }
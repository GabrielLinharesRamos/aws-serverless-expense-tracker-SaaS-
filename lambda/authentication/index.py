# from services.login import login
from services.signup import signup

def lambda_handler(event, context):

    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]

    if method == "POST" and path == "/dev/auth/signup":
        return signup(event)

    elif method == "POST" and path == "/dev/auth/signup":
        return login(event)

    return {
        "statusCode": 405,
        "body": "Method Not Allowed"
    }
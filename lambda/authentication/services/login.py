import boto3
import json
import os
import logging

from shared.validators.allowed_fields_validator import validate_fields

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cognito = boto3.client("cognito-idp")

def login(event):
    try:

        body = json.loads(event["body"])
        email = body["email"]
        password = body["password"]

        allowed_fields = {"email", "password"}

        validate_fields(body, allowed_fields)

        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            },
            ClientId=os.environ["COGNITO_CLIENT_ID"]
        )

        return {
            'statusCode': 200,
            "body": json.dumps({
                "message": "logged in",
                "tokens": response["AuthenticationResult"]
            })
        }

    except Exception as e:
        logger.error(
            json.dumps(
                {
                    "message": "Failed to log in the user",
                    "request_id": event["requestContext"]["requestId"],
                    "event_type": 'login_user',
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
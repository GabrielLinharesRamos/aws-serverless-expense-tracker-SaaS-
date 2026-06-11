import boto3
import os
from datetime import datetime

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["EXPENSES_TABLE"]
)

def save(item):
    table.put_item(Item=item)

def list_by_user(user_id):
    response = table.query(KeyConditionExpression=Key('PK').eq(f"USER#{user_id}"))

    return response["Items"]

def exclude_expense_repository(user_id, expense_id):
    table.delete_item(
        Key={
            "PK": f"USER#{user_id}",
            "SK": f"EXPENSE#{expense_id}"
        },
        ConditionExpression="attribute_exists(PK)"
    )

def update_expense_repository(user_id,expense_id,amount,description):
    table.update_item(
        Key={
            "PK": f"USER#{user_id}",
            "SK": f"EXPENSE#{expense_id}"
        },
        UpdateExpression="""
            SET amount = :amount,
                description = :description,
                updated_at = :updated_at
        """,
        ExpressionAttributeValues={
            ':amount': amount,
            ':description': description,
            ':updated_at': datetime.utcnow().isoformat()
        },
        ConditionExpression="attribute_exists(PK)"
    )
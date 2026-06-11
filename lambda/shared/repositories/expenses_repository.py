import boto3
import os

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
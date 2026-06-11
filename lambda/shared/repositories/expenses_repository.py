import boto3
import os

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["EXPENSES_TABLE"]
)

def save(item):
    table.put_item(Item=item)

def list_by_user(username):
    response = table.query(KeyConditionExpression=Key('PK').eq(username))

    return response["Items"]
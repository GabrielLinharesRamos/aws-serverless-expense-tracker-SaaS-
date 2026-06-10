import boto3
import os

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(
    os.environ["EXPENSES_TABLE"]
)

def save(item):
    table.put_item(Item=item)
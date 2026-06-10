from service import create_expense

def lambda_handler(event, context):
    return create_expense(event)
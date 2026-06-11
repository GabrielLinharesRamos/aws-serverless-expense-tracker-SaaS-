from service import list_expense

def lambda_handler(event, context):
    return list_expense(event)
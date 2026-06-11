from service import update_expense

def lambda_handler(event, context):
    return update_expense(event)
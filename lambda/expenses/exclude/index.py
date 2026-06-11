from service import exclude_expense

def lambda_handler(event, context):
    return exclude_expense(event)
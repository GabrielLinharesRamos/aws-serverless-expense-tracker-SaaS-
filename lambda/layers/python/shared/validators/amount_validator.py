from decimal import Decimal

def validate_amount(amount):

    try:
        return Decimal(amount)

    except (ValueError, TypeError):
        raise ValueError(
            "amount must be a valid number"
        )
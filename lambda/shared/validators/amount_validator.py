def validate_amount(amount):

    try:
        return float(amount)

    except (ValueError, TypeError):
        raise ValueError(
            "amount must be a valid number"
        )
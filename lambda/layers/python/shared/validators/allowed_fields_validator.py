def validate_fields(body: dict, allowed_fields: set):

    received_fields = set(body.keys())

    if received_fields != allowed_fields:
        raise ValueError(
            f"Only these fields are allowed: {allowed_fields}"
        )
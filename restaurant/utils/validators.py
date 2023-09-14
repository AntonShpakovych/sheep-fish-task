from typing import Dict, Type

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from rest_framework.serializers import ValidationError as DRFError

from restaurant.utils.schemas import ORDER_SCHEMA


def validate_order_value(value: Dict, error_to_raise: Type[DRFError]):
    """
    Validate the order data against a schema and raise
    an error if validation fails.

    This function validates the provided order data against
    a predefined schema.
    If the validation fails, it raises an error of the specified
    type with a descriptive message.

    :param value: The order data to validate.
    :type value: dict
    :param error_to_raise: The type of error to raise if validation fails (e.g., serializers.ValidationError). # noqa: 501
    :type error_to_raise: Type[DRFValidationError]
    :raises error_to_raise: If validation against the schema fails.
    """
    message_schema = {
        "point_id": 1,
        "items": [
            {
                "product_id": 1,
                "quantity": 1,
                "unit_price": 10.5
            }
        ]
    }

    try:
        validate(value, ORDER_SCHEMA)
    except ValidationError:
        raise error_to_raise(
            "Order schema should equal to: "
            f"{message_schema}"
        )

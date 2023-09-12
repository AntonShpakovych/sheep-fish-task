from jsonschema import validate
from jsonschema.exceptions import ValidationError

from restaurant.utils.schemas import ORDER_SCHEMA


def validate_order_value(value, error_to_raise):
    try:
        validate(value, ORDER_SCHEMA)
    except ValidationError:
        raise error_to_raise(
            "Order schema should equal to: "
            f"{ORDER_SCHEMA}"
        )

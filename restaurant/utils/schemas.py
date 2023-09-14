ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "point_id": {"type": "integer"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "quantity": {"type": "integer"},
                    "unit_price": {"type": "number"}
                },
                "required": ["product_id", "quantity", "unit_price"]
            }
        }
    },
    "required": ["point_id", "items"]
}

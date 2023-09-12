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
                },
                "required": ["product_id", "quantity"]
            }
        }
    },
    "required": ["point_id", "items"]
}

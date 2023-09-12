from rest_framework import serializers

from restaurant.utils.validators import validate_order_value


class OrderSerializer(serializers.Serializer):
    order = serializers.JSONField()

    def validate_order(self, value):
        validate_order_value(
            value=value,
            error_to_raise=serializers.ValidationError
        )

        return value

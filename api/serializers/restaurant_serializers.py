from typing import Dict

from rest_framework import serializers

from restaurant.models import Check, Printer, Point
from restaurant.utils.validators import validate_order_value


class OrderSerializer(serializers.Serializer):
    """
    Serializer for an 'order' object.

    This serializer is used to validate and deserialize an 'order' object,
    which is expected to be a dictionary.

    Example usage:
    ```
    serializer = OrderSerializer(data={'order': some_order_data})
    if serializer.is_valid():
        validated_order = serializer.validated_data['order']
    ```

    :param serializers.Serializer: The base serializer class.
    """
    order = serializers.JSONField()

    def validate_order(self, value: Dict):
        """
        Validate the 'order' field.

        :param value: The value of the 'order' field.
        :type value: dict
        :return: The validated 'order' value.
        :rtype: dict
        :raises serializers.ValidationError: If validation fails.
        """
        validate_order_value(
            value=value,
            error_to_raise=serializers.ValidationError
        )

        return value


class CheckListSerializer(serializers.ModelSerializer):
    """
    Serializer for a list of Check objects.

    This serializer is used to serialize a list of Check
    objects with the following fields:
    - id (int): The unique identifier of the Check.
    - type (str): The type of the Check.
    - status (str): The status of the Check.

    Example usage:
    ```
    serializer = CheckListSerializer(queryset, many=True)
    serialized_data = serializer.data.
    ```

    :param serializers.ModelSerializer: The base model serializer class.
    """
    class Meta:
        model = Check
        fields = ["id", "type", "status"]


class CheckDetailSerializer(CheckListSerializer):
    """
    Serializer for detailed representation of a Check instance.

    This serializer is used to provide a detailed representation of a Check
    instance, including additional fields such as 'printer' and 'order'.

    Example usage:
    ```
    serializer = CheckDetailSerializer(instance=check_instance)
    serialized_data = serializer.data.
    ```

    :param CheckListSerializer: The base serializer class for listing Check.
    """

    class Meta(CheckListSerializer.Meta):
        fields = CheckListSerializer.Meta.fields + [
            "printer", "order"
        ]


class PrinterListSerializer(serializers.ModelSerializer):
    """
    Serializer for a list of Printer objects.

    This serializer is used to serialize a list of Printer objects
    with the following fields:
    - id (int): The unique identifier of the Printer.
    - api_key (str): The API key associated with the Printer.
    - check_type (str): The type of checks handled by the Printer.

    Example usage:
    ```
    serializer = PrinterListSerializer(queryset, many=True)
    serialized_data = serializer.data.
    ```

    :param serializers.ModelSerializer: The base model serializer class.
    """
    class Meta:
        model = Printer
        fields = ["id", "api_key", "check_type"]


class PrinterDetailSerializer(PrinterListSerializer):
    """
    Serializer for detailed representation of a Printer instance.

    This serializer is used to provide a detailed representation of a Printer
    instance, including additional fields such as 'point' and 'checks'.

    Example usage:
    ```
    serializer = PrinterDetailSerializer(instance=printer_instance)
    serialized_data = serializer.data.
    ```

    :param PrinterListSerializer: The base serializer class for listing Printer objects.# noqa: 501
    """
    class Meta(PrinterListSerializer.Meta):
        fields = PrinterListSerializer.Meta.fields + [
            "point", "checks"
        ]


class PointListSerializer(serializers.ModelSerializer):
    """
    Serializer for a list of Point objects.

    This serializer is used to serialize a list of Point
    objects with the following fields:
    - id (int): The unique identifier of the Point.
    - name (str): The name of the Point.
    - address (str): The address of the Point.

    Example usage:
    ```
    serializer = PointListSerializer(queryset, many=True)
    serialized_data = serializer.data.
    ```

    :param serializers.ModelSerializer: The base model serializer class.
    """
    class Meta:
        model = Point
        fields = ["id", "name", "address"]


class PointDetailSerializer(PointListSerializer):
    """
    Serializer for detailed representation of a Point instance.

    This serializer is used to provide a detailed representation of a
    Point instance, including additional fields such as 'printers'.

    Example usage:
    ```
    serializer = PointDetailSerializer(instance=point_instance)
    serialized_data = serializer.data.
    ```

    :param PointListSerializer: The base serializer class for listing Point objects. # noqa: 501
    """
    class Meta(PointListSerializer.Meta):
        fields = PointListSerializer.Meta.fields + [
            "printers"
        ]

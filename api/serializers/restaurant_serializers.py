from rest_framework import serializers

from restaurant.models import Check, Printer, Point
from restaurant.utils.validators import validate_order_value


class OrderSerializer(serializers.Serializer):
    order = serializers.JSONField()

    def validate_order(self, value):
        validate_order_value(
            value=value,
            error_to_raise=serializers.ValidationError
        )

        return value


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ["id", "type", "status"]


class CheckDetailSerializer(CheckListSerializer):
    class Meta(CheckListSerializer.Meta):
        fields = CheckListSerializer.Meta.fields + [
            "printer", "order"
        ]


class PrinterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ["id", "api_key", "check_type"]


class PrinterDetailSerializer(PrinterListSerializer):
    class Meta(PrinterListSerializer.Meta):
        fields = PrinterListSerializer.Meta.fields + [
            "point", "checks"
        ]


class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ["id", "name", "address"]


class PointDetailSerializer(PointListSerializer):
    class Meta(PointListSerializer.Meta):
        fields = PointListSerializer.Meta.fields + [
            "printers"
        ]

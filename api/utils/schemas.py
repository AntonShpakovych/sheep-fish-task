from rest_framework import serializers

from drf_spectacular.utils import OpenApiParameter, inline_serializer

from api.serializers.restaurant_serializers import (
    CheckListSerializer,
    PrinterListSerializer,
    PrinterDetailSerializer,
    PointListSerializer,
    PointDetailSerializer
)
from api.utils import check_messages, printer_messages


CHECK_CREATE_LIST_GET_SCHEMA = {
        "description": "Retrieve a list of checks with optional filtering by status",
        "parameters": [
            OpenApiParameter(
                name="status",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter checks by status"
            )
        ],
        "responses": {
            200: CheckListSerializer(many=True),
        }
}
CHECK_CREATE_LIST_POST_SCHEMA = {
    "description": "Create a new check",
    "request": inline_serializer(
        name="creat_check",
        fields={
            "order": serializers.JSONField(
                default={
                    "point_id": 1,
                    "items": [
                        {
                            "product_id": 1,
                            "quantity": 1,
                            "unit_price": 1
                        }
                    ]
                }
            ),
        },
    ),
    "responses": {
        201: inline_serializer(
            name="return_creting_checks",
            fields={
                "kitchen": serializers.IntegerField(default=1),
                "client": serializers.IntegerField(default=1)
            }
        ),
        400: inline_serializer(
            name="return_invalid_message",
            fields={
                "When point without printers": serializers.CharField(
                    default=check_messages.CHECK_CREATE_INVALID
                ),
                "When order invalid": serializers.CharField(
                    default="""Order schema should equal to: {order: {point_id: 1, items: [{product_id: 1, quantity: 1, unit_price: 1}]}}"""
                )
            }
        )
    }
}

CHECK_DETAIL_GET_SCHEMA = {
    "description": "Retrieve details of a single check and its associated printer",
    "responses": {
        200: inline_serializer(
            name="get_single_check",
            fields={
                "When all good": serializers.JSONField(
                    default={
                        "id": 1,
                        "type": "client",
                        "status": "new",
                        "printer": 1,
                        "order": {
                            "point_id": 1,
                            "items": [
                                {"product_id": 1,
                                 "quantity": 1,
                                 "unit_price": 1
                                 }
                            ]
                        }
                    }
                )
            }
        )
    }
}

CHECK_TO_PDF_POST_SCHEMA = {
    "description":"Check to PDF file",
    "responses": {
        200: inline_serializer(
            name="valid_check",
            fields={
                "When valid": serializers.CharField(default=check_messages.CHECK_TO_PDF_SUCCESS)
            }
        ),
        400: inline_serializer(
            name="invalid_check",
            fields={
                "When invalid": serializers.CharField(default=check_messages.CHECK_TO_PDF_INVALID)
            }
        )
    }
}

PRINTER_PRINT_PDF_POST_SCHEMA = {
    "description": "Printer print PDF checks",
    "responses": {
        200: inline_serializer(
            name="valid_printer",
            fields={
                "When valid": serializers.CharField(default=printer_messages.PRINTER_PRINT_PDF_VALID_MESSAGE)
            }
            ),
        400: inline_serializer(
            name="invalid_printer",
            fields={
                "When invalid": serializers.CharField(default=printer_messages.PRINTER_PRINT_PDF_INVALID)
            }
        )
    }
}

PRINTER_LIST_GET_SCHEMA = {
    "description": "Retrieve a list of printers with optional filtering by check type",
    "parameters": [
        OpenApiParameter(
            name="check_type",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter printers by check type"
        )
    ],
    "responses": {200: PrinterListSerializer(many=True)}
}

PRINTER_DETAIL_GET_SCHEMA = {
    "description": "Retrieve details of a single printer and its associated point and checks",
    "responses": {200: PrinterDetailSerializer}
}

POINT_LIST_GET_SCHEMA = {
    "description": "Retrieve a list of points with optional filtering by name and address",
    "parameters": [
        OpenApiParameter(
            name="name",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter points by name (case-insensitive)"
        ),
        OpenApiParameter(
            name="address",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter points by address (case-insensitive)"
        )
    ],
    "responses": {200: PointListSerializer(many=True)}
}

POINT_DETAIL_GET_SCHEMA = {
    "description": "Retrieve a single point and its associated printers",
    "responses": {200: PointDetailSerializer}
}

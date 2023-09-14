from rest_framework import views, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema

from api.utils import check_messages, printer_messages
from api.serializers.restaurant_serializers import (
    OrderSerializer,
    CheckListSerializer,
    CheckDetailSerializer,
    PrinterListSerializer,
    PrinterDetailSerializer,
    PointListSerializer,
    PointDetailSerializer
)
from api.utils.schemas import (
    CHECK_CREATE_LIST_GET_SCHEMA,
    CHECK_DETAIL_GET_SCHEMA,
    CHECK_TO_PDF_POST_SCHEMA,
    PRINTER_PRINT_PDF_POST_SCHEMA,
    PRINTER_LIST_GET_SCHEMA,
    PRINTER_DETAIL_GET_SCHEMA,
    POINT_LIST_GET_SCHEMA,
    POINT_DETAIL_GET_SCHEMA,
    CHECK_CREATE_LIST_POST_SCHEMA
)

from restaurant.models import Check, Printer, Point
from restaurant.tasks import produce_print

from services.check_to_pdf_service import CheckToPDFService
from services.erp_service import ErpService
from services.print_check_pdf_service import PrintCheckPDFService


@extend_schema(tags=["Check"])
class CheckCreateListAPIView(views.APIView):
    """
    API view for creating and listing Check instances.
    """
    @extend_schema(**CHECK_CREATE_LIST_GET_SCHEMA)
    def get(self, request: Request) -> Response:
        """
        Get a list of Check instances or filter by status.

        :param request: The HTTP request object.
        :return: A Response with serialized Check data.
        """
        queryset = Check.objects.all()
        status_param = self.request.query_params.get("status")

        if status_param:
            queryset = queryset.filter(status=status_param)

        serializer = CheckListSerializer(
            queryset,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(**CHECK_CREATE_LIST_POST_SCHEMA)
    def post(self, request: Request) -> Response:
        """
        Create a new Check instances.

        :param request: The HTTP request object.
        :return: A Response with Check ({"type": id}) or 400 Bad Request.
        """
        order_serializer = OrderSerializer(data=request.data)

        if order_serializer.is_valid():
            checks = ErpService.create_check(order=order_serializer.data)

            if checks:
                return Response(
                    checks,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                check_messages.CHECK_CREATE_INVALID,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            order_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=["Check"],
    **CHECK_DETAIL_GET_SCHEMA
)
class CheckDetailAPIView(views.APIView):
    """
    API view for retrieving details of a Check instance.
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        Get the details of a Check instance by its primary key.

        :param request: The HTTP request object.
        :param pk: The primary key of the Check instance.
        :return: A Response with serialized Check data or 404 if not found.
        """
        check = get_object_or_404(
            Check.objects.select_related("printer"),
            pk=pk
        )
        serializer = CheckDetailSerializer(check, many=False)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Check"],
    **CHECK_TO_PDF_POST_SCHEMA
)
class CheckToPDFApiView(views.APIView):
    """
    API view for generating a PDF from a Check instance.
    """
    def post(self, request: Request, pk: int) -> Response:
        """
        Generate a PDF from a Check instance.

        :param request: The HTTP request object.
        :param pk: The primary key of the Check instance.
        :return: A Response indicating the result of PDF generation.
        """
        check = get_object_or_404(Check, id=pk)

        if CheckToPDFService.is_file_already_exist(check=check):
            return Response(
                check_messages.CHECK_TO_PDF_INVALID,
                status=status.HTTP_400_BAD_REQUEST
            )

        CheckToPDFService.generate_pdf(pk=pk)

        return Response(
            check_messages.CHECK_TO_PDF_SUCCESS,
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Printer"],
    **PRINTER_PRINT_PDF_POST_SCHEMA
)
class PrinterPrintPDFApiView(views.APIView):
    """
    API view for printing PDFs from a Printer instance.
    """
    def post(self, request: Request, pk: int) -> Response:
        """
        Print PDFs from a Printer instance.

        :param request: The HTTP request object.
        :param pk: The primary key of the Printer instance.
        :return: A Response indicating the result of PDF printing.
        """
        printer = get_object_or_404(
            Printer.objects.prefetch_related("checks"),
            pk=pk
        )
        rendered_checks_ids = PrintCheckPDFService.get_rendered_checks(
            printer=printer
        )

        if rendered_checks_ids:
            produce_print.delay(check_ids=rendered_checks_ids)

            return Response(
                printer_messages.PRINTER_PRINT_PDF_VALID_MESSAGE,
                status=status.HTTP_200_OK
            )

        return Response(
            printer_messages.PRINTER_PRINT_PDF_INVALID,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=["Printer"],
    **PRINTER_LIST_GET_SCHEMA
)
class PrinterListView(generics.ListAPIView):
    """
    API view for listing printers with optional filtering by check_type.
    """
    serializer_class = PrinterListSerializer

    def get_queryset(self):
        """
        Get the queryset of printers, optionally filtered by check type.

        :return: A queryset of printers.
        """
        check_type_param = self.request.query_params.get("check_type")
        queryset = Printer.objects.all()

        if check_type_param:
            queryset = queryset.filter(check_type=check_type_param)

        return queryset


@extend_schema(
    tags=["Printer"],
    **PRINTER_DETAIL_GET_SCHEMA
)
class PrinterDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a Printer instance.
    """
    serializer_class = PrinterDetailSerializer
    queryset = Printer.objects.select_related(
        "point"
    ).prefetch_related("checks")


@extend_schema(
    tags=["Point"],
    **POINT_LIST_GET_SCHEMA
)
class PointListView(generics.ListAPIView):
    """
    API view for listing points with optional filtering by name and address.
    """
    serializer_class = PointListSerializer

    def get_queryset(self):
        """
        Get the queryset of points, optionally filtered by name and address.

        :return: A queryset of points.
        """
        queryset = Point.objects.all()

        name_param = self.request.query_params.get("name")
        address_param = self.request.query_params.get("address")

        if address_param:
            queryset = queryset.filter(address__icontains=address_param)

        if name_param:
            queryset = queryset.filter(name__icontains=name_param)

        return queryset


@extend_schema(
    tags=["Point"],
    **POINT_DETAIL_GET_SCHEMA
)
class PointDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a Point instance.
    """
    serializer_class = PointDetailSerializer
    queryset = Point.objects.prefetch_related("printers")

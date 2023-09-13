from rest_framework import views, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

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

from restaurant.models import Check, Printer, Point
from restaurant.tasks import produce_print

from services.check_to_pdf_service import CheckToPDFService
from services.erp_service import ErpService
from services.print_check_pdf_service import PrintCheckPDFService


class CheckCreateListAPIView(views.APIView):
    def get(self, request):
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

    def post(self, request):
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


class CheckDetailAPIView(views.APIView):
    def get(self, request, check_id):
        check = get_object_or_404(
            Check.objects.select_related("printer"),
            id=check_id
        )
        serializer = CheckDetailSerializer(check, many=False)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CheckToPDFApiView(views.APIView):
    def post(self, request, check_id):
        check = get_object_or_404(Check, id=check_id)

        if CheckToPDFService.is_file_already_exist(check):
            return Response(
                check_messages.CHECK_TO_PDF_INVALID,
                status=status.HTTP_400_BAD_REQUEST
            )

        CheckToPDFService.generate_pdf(check_id)

        return Response(
            check_messages.CHECK_TO_PDF_SUCCESS,
            status=status.HTTP_200_OK
        )


class PrinterPrintPDFApiView(views.APIView):
    def post(self, request, printer_id):
        printer = get_object_or_404(
            Printer.objects.prefetch_related("checks"),
            id=printer_id
        )
        rendered_checks = PrintCheckPDFService.get_rendered_checks(
            printer=printer
        )

        if rendered_checks:
            produce_print.delay(rendered_checks)

            return Response(
                printer_messages.PRINTER_PRINT_PDF_VALID_MESSAGE,
                status=status.HTTP_200_OK
            )

        return Response(
            printer_messages.PRINTER_PRINT_PDF_INVALID,
            status=status.HTTP_400_BAD_REQUEST
        )


class PrinterListView(generics.ListAPIView):
    serializer_class = PrinterListSerializer

    def get_queryset(self):
        check_type_param = self.request.query_params.get("check_type")
        queryset = Printer.objects.all()

        if check_type_param:
            queryset = queryset.filter(check_type=check_type_param)

        return queryset


class PrinterDetailView(generics.RetrieveAPIView):
    serializer_class = PrinterDetailSerializer
    queryset = Printer.objects.select_related(
        "point"
    ).prefetch_related("checks")


class PointListView(generics.ListAPIView):
    serializer_class = PointListSerializer

    def get_queryset(self):
        queryset = Point.objects.all()

        name_param = self.request.query_params.get("name")
        address_param = self.request.query_params.get("address")

        if address_param:
            queryset = queryset.filter(address__icontains=address_param)

        if name_param:
            queryset = queryset.filter(name__icontains=name_param)

        return queryset


class PointDetailView(generics.RetrieveAPIView):
    serializer_class = PointDetailSerializer
    queryset = Point.objects.prefetch_related("printers")

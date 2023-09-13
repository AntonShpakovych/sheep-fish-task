from rest_framework import views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.utils import check_messages, printer_messages
from api.serializers.restaurant_serializers import OrderSerializer

from restaurant.models import Check, Printer
from restaurant.tasks import produce_print

from services.check_to_pdf_service import CheckToPDFService
from services.erp_service import ErpService
from services.print_check_pdf_service import PrintCheckPDFService


class CheckCreateAPIView(views.APIView):
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

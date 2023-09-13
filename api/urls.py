from django.urls import path

from api.views import (
    CheckCreateAPIView,
    CheckToPDFApiView,
    PrinterPrintPDFApiView
)


urlpatterns = [
    path(
        "checks/",
        CheckCreateAPIView.as_view(),
        name="checks"
    ),
    path(
        "checks/<int:check_id>/generate-pdf/",
        CheckToPDFApiView.as_view(),
        name="check-generate-pdf"
    ),
    path(
        "printers/<int:printer_id>/print-pdf/",
        PrinterPrintPDFApiView.as_view(),
        name="printer-print-pdf"
    )
]

app_name = "api"

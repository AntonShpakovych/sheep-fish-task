from django.urls import path

from api.views import (
    CheckCreateListAPIView,
    CheckDetailAPIView,
    CheckToPDFApiView,
    PrinterListView,
    PrinterPrintPDFApiView,
    PrinterDetailView,
    PointListView,
    PointDetailView
)


urlpatterns = [
    path(
        "checks/",
        CheckCreateListAPIView.as_view(),
        name="check-list"
    ),
    path(
        "checks/<int:check_id>/",
        CheckDetailAPIView.as_view(),
        name="check-detail"
    ),
    path(
        "checks/<int:check_id>/generate-pdf/",
        CheckToPDFApiView.as_view(),
        name="check-generate-pdf"
    ),
    path(
        "printers/",
        PrinterListView.as_view(),
        name="printer-list"
    ),
    path(
        "printers/<int:pk>/",
        PrinterDetailView.as_view(),
        name="printer-detail"
    ),
    path(
        "printers/<int:printer_id>/print-pdf/",
        PrinterPrintPDFApiView.as_view(),
        name="printer-print-pdf"
    ),
    path(
        "points/",
        PointListView.as_view(),
        name="point-list"
    ),
    path(
        "points/<int:pk>/",
        PointDetailView.as_view(),
        name="point-detail"
    )
]

app_name = "api"

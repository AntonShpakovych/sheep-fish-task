from django.urls import path

from api.views import (
    CheckCreateAPIView,
    CheckToPDFApiView
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
    )
]

app_name = "api"

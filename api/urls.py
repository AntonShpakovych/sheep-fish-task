from django.urls import path

from api.views import CheckCreateAPIView


urlpatterns = [
    path(
        "checks/",
        CheckCreateAPIView.as_view(),
        name="checks"
    )
]

app_name = "api"

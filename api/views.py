from rest_framework import views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from restaurant.models import Check

from services.check_to_pdf_service import CheckToPDFService
from services.erp import ErpService

from api.serializers.restaurant_serializers import OrderSerializer


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
                "The specified point is invalid or has no printers",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            order_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CheckToPDFApiView(views.APIView):
    def post(self, request, check_id):
        check = get_object_or_404(Check, id=check_id)

        if CheckToPDFService.is_already_exist(check=check):
            return Response(
                f"{check.id}__{check.type}.pdf already exists",
                status=status.HTTP_400_BAD_REQUEST
            )

        CheckToPDFService.generate_pdf(check)

        return Response(
            "The check to pdf generation task has been sent",
            status=status.HTTP_200_OK
        )

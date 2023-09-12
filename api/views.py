from rest_framework import views, status
from rest_framework.response import Response

from api.serializers.restaurant_serializers import OrderSerializer
from services.erp import ErpService


class CheckCreateAPIView(views.APIView):
    def post(self, request):
        order_serializer = OrderSerializer(data=request.data)

        if order_serializer.is_valid():
            checks = ErpService.create_check(order=order_serializer.data)

            if checks:
                return Response(
                    "Checks for all point printers are created",
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

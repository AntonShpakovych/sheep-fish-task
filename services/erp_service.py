from typing import Dict, Any

from restaurant.models import Check, Point


class ErpService:
    """
    Service for creating check
    """
    @classmethod
    def create_check(cls, order: Dict[str, Any]) -> Dict[str, int]:
        """
        Create checks for an order and
        return a dictionary of created check IDs.

        This method takes an order dictionary and creates checks
        for each printer associated with the order's point.
        It returns a dictionary where keys are check types,
        and values are check ID.

        :param order: The order data containing 'point_id' and other relevant information. # noqa: 501
        :type order: dict
        :return: A dictionary of created check IDs grouped by check type.
        :rtype: dict
        """
        order_data = order["order"]
        order_point_id = order_data["point_id"]

        check_point = Point.objects.filter(id=order_point_id)

        if check_point:
            point = check_point.first()

            return {
                check.type: check.id for check in
                [
                    Check.objects.create(
                        printer=printer,
                        type=printer.check_type,
                        order=order_data
                    )
                    for printer in point.printers.all()
                ]
            }
        return {}

from restaurant.models import Check, Point


class ErpService:
    @classmethod
    def create_check(cls, order):
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

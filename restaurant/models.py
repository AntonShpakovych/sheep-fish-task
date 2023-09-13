from django.db import models

from restaurant.utils.upload_to import pdf_path
from restaurant.utils.choices import (
    PrinterCheckTypeChoices,
    CheckTypeChoices,
    CheckStatusChoices
)


class Point(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Printer(models.Model):
    name = models.CharField(max_length=30)
    api_key = models.CharField(max_length=36, unique=True)
    check_type = models.CharField(
        max_length=7,
        choices=PrinterCheckTypeChoices.choices
    )
    point = models.ForeignKey(
        Point,
        related_name="printers",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Check(models.Model):
    printer = models.ForeignKey(
        Printer,
        related_name="checks",
        on_delete=models.SET_NULL,
        null=True
    )
    type = models.CharField(
        max_length=7,
        choices=CheckTypeChoices.choices
    )
    status = models.CharField(
        max_length=8,
        choices=CheckStatusChoices.choices,
        default=CheckStatusChoices.NEW
    )
    pdf_file = models.FileField(
        upload_to=pdf_path,
        blank=True,
        null=True
    )
    order = models.JSONField()

    def __str__(self):
        return f"check_{self.id}"

    @property
    def full_price(self):
        return sum(
            order_item["quantity"] * order_item["unit_price"]
            for order_item in self.order["items"]
        )

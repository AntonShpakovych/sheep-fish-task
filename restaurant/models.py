from django.db import models

from restaurant.utils.upload_to import pdf_path
from restaurant.utils.choices import (
    PRINTER_CHECK_TYPE_CHOICES,
    CHECK_TYPE_CHOICES,
    CHECK_STATUS_CHOICES
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
        choices=PRINTER_CHECK_TYPE_CHOICES
    )
    point = models.ForeignKey(
        Point,
        related_name="printers",
        on_delete=models.CASCADE
    )


class Check(models.Model):
    printer = models.ForeignKey(
        Printer,
        related_name="checks",
        on_delete=models.SET_NULL,
        null=True
    )
    type = models.CharField(
        max_length=7,
        choices=CHECK_TYPE_CHOICES
    )
    status = models.CharField(
        max_length=8,
        choices=CHECK_STATUS_CHOICES
    )
    pdf_file = models.FileField(
        upload_to=pdf_path,
        blank=True,
        null=True
    )
    order = models.JSONField()

    def __str__(self):
        return f"check_{self.id}"

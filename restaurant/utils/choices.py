from django.db import models


class CheckStatusChoices(models.TextChoices):
    NEW = ("new", "new")
    RENDERED = ("rendered", "rendered")
    PRINTED = ("printed", "printed")


class PrinterCheckTypeChoices(models.TextChoices):
    CLIENT = ("client", "client")
    KITCHEN = ("kitchen", "kitchen")


class CheckTypeChoices(models.TextChoices):
    CLIENT = ("client", "client")
    KITCHEN = ("kitchen", "kitchen")

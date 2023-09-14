from django.contrib import admin

from restaurant.models import Printer, Check, Point


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ["printer", "type", "status"]


admin.site.register(Printer)
admin.site.register(Point)

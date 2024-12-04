from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'instrument', 'unit_price', 'quantity', 'total_price', 'settled_at')

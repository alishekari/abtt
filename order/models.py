from django.db import models

from utils.mixins.modification.models import ModificationMixin


class Order(ModificationMixin, models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="orders")
    instrument = models.ForeignKey("instrument.Instrument", on_delete=models.CASCADE, related_name="orders")
    unit_price = models.PositiveIntegerField()
    quantity = models.FloatField()
    total_price = models.PositiveIntegerField()
    settled_at = models.DateTimeField(null=True, blank=True)

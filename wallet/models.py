from django.db import models

from utils.mixins.modification.models import ModificationMixin
from wallet.enums import StatementType


class Wallet(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    withdrawable_balance = models.IntegerField(default=0)


class Statement(ModificationMixin):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='statements')
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=8, choices=StatementType.choices)
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=1024, blank=True, null=True)
    tracking_code = models.CharField(max_length=128, blank=True, null=True)
    balance = models.IntegerField(default=0)

    class Meta:
        ordering = ('-_created_at',)

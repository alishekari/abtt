import typing

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from AbanTether.constants import MINIMUM_OKX_AMOUNT
from exchange.services.settlement_services import SettlementServices
from instrument.services.instrument_services import InstrumentServices
from order.models import Order
from wallet.services.statement_services import StatementServices
from wallet.services.wallet_services import WalletServices

if typing.TYPE_CHECKING:
    from instrument.models import Instrument
    from user.models import User


class OrderServices:
    def __init__(self, order: Order):
        self.order = order

    @classmethod
    def make_order(cls, user: 'User', instrument: 'Instrument', quantity: int):
        price = InstrumentServices(instrument=instrument).get_online_price()
        total_price = price * quantity

        if not WalletServices.does_wallet_can_be_debit_by_client_id_and_amount(
                user_id=user.id,
                amount=total_price
        ):
            raise ValueError('Wallet does not have enough balance.')

        with transaction.atomic():
            order = Order.objects.create(user=user, instrument=instrument, unit_price=price, quantity=quantity,
                                         total_price=total_price)
            StatementServices.create_order_statement(order_id=order.id, amount=total_price)

            if total_price >= MINIMUM_OKX_AMOUNT:
                SettlementServices.buy_from_exchange(instrument_slug=instrument.name, amount=quantity)
                order.settled_at = timezone.now()
                order.save(update_fields=['settled_at'])
            else:
                # should be done in a separate task in celery
                cls.settle_unsettled_orders(instrument=instrument)
        return order

    @classmethod
    def get_wallet_id_of_order_by_order_id(cls, order_id) -> int:
        order = cls._get_order_by_id(order_id=order_id)
        return cls(order=order)._get_wallet_id_of_order()

    @staticmethod
    def _get_order_by_id(order_id: int) -> Order:
        return Order.objects.get(id=order_id)

    @classmethod
    def settle_unsettled_orders(cls, instrument: 'Instrument'):
        if cls.inquiry_not_settled_orders_amount(instrument=instrument) >= MINIMUM_OKX_AMOUNT:
            now = timezone.now()
            orders = Order.objects.filter(instrument=instrument, settled_at__isnull=True)
            with transaction.atomic():
                for order in orders:
                    order.settled_at = now
                    order.save(update_fields=['settled_at'])
                SettlementServices.buy_from_exchange(
                    instrument_slug=instrument.name,
                    amount=orders.aggregate(total_amount=Sum('total_price'))
                )

    @staticmethod
    def inquiry_not_settled_orders_amount(instrument: 'Instrument'):
        return Order.objects.filter(instrument=instrument, settled_at__isnull=True).aggregate(
            total_amount=Sum('total_price', default=0)
        )['total_amount']

    def _get_wallet_id_of_order(self) -> int:
        return self.order.user.wallet.id

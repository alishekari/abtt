from django.db.models import QuerySet

from wallet.enums import StatementType
from wallet.models import Statement, Wallet
from django.db import transaction


class StatementServices:
    def __init__(self, statement: Statement):
        self.statement = statement

    @classmethod
    def create_order_statement(cls, order_id, amount: int) -> Statement:
        from order.services.order_services import OrderServices

        if amount <= 0:
            raise ValueError('Amount should be greater than 0')

        wallet_id = OrderServices.get_wallet_id_of_order_by_order_id(order_id=order_id)
        return cls._create_statement(
            wallet_id=wallet_id,
            amount=amount,
            order_id=order_id,
            statement_type=StatementType.DEBIT
        )

    @classmethod
    def _create_statement(
            cls,
            wallet_id: int,
            amount: int,
            statement_type: StatementType,  # credit or debit
            order_id: int = None,  # order
            comment: str = None,
            tracking_code: str = None,
    ) -> Statement:

        if amount <= 0:
            raise ValueError('Amount should be greater than 0')

        wallet = Wallet.objects.get(id=wallet_id)

        if statement_type == StatementType.DEBIT and wallet.balance < amount:
            raise ValueError('Not enough balance')


        with transaction.atomic():
            statement = Statement.objects.create(
                wallet_id=wallet_id,
                amount=amount,
                type=statement_type,
                order_id=order_id,
                comment=comment,
                tracking_code=tracking_code,
            )

            if statement.type == StatementType.DEBIT:
                if wallet.withdrawable_balance >= statement.amount:
                    wallet.withdrawable_balance -= statement.amount
                else:
                    remaining_amount = statement.amount - wallet.withdrawable_balance
                    wallet.withdrawable_balance = 0
                    wallet.non_withdrawable_balance -= remaining_amount
            elif statement.type == StatementType.CREDIT:
                pass
            wallet.save()
            statement.balance = wallet.balance
            statement.save()
        return statement

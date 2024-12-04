from wallet.models import Wallet


class WalletServices:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    @staticmethod
    def _get_wallet_by_user_id(user_id: int) -> Wallet:
        return Wallet.objects.get_or_create(user_id=user_id)[0]

    @classmethod
    def get_wallet_id_by_client_id(cls, user_id: int) -> int:
        return cls._get_wallet_by_user_id(user_id=user_id).id

    @classmethod
    def does_wallet_can_be_debit_by_client_id_and_amount(cls, user_id: int, amount: int) -> bool:
        wallet = cls._get_wallet_by_user_id(user_id=user_id)
        return wallet.withdrawable_balance >= amount

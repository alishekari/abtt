from wallet.models import Wallet


class CurrentWalletDefault:
    requires_context = True

    def __call__(self, serializer_field):
        try:
            return serializer_field.context['request'].user.client.wallet
        except Wallet.DoesNotExist:
            return Wallet.objects.create(client=serializer_field.context['request'].user.client)

    def __repr__(self):
        return '%s()' % self.__class__.__name__

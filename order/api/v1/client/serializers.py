from rest_framework import serializers

from instrument.models import Instrument
from order.models import Order
from order.services.order_services import OrderServices


class OrderSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'instrument': 'Instrument not found.'
    }

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    instrument_name = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'instrument_name', 'quantity']

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        try:
            data['instrument'] = Instrument.objects.get(name=data.pop('instrument_name'))
        except Instrument.DoesNotExist:
            self.fail('instrument')
        return data

    def create(self, validated_data):
        return OrderServices.make_order(user=validated_data['user'], instrument=validated_data['instrument'],
                                        quantity=validated_data['quantity'])

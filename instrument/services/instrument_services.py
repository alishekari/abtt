import typing
from random import randint

if typing.TYPE_CHECKING:
    from instrument.models import Instrument

class InstrumentServices:
    def __init__(self, instrument: 'Instrument'):
        self.instrument = instrument

    def get_online_price(self) -> int:
        """
        The method for retrieve online price of Instrument
        :return: Online Price
        """
        return self._fake_price_generator()

    @staticmethod
    def _fake_price_generator() -> int:
        return randint(1000, 10000)

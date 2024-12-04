from django.db import models

from instrument.services.instrument_services import InstrumentServices


class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @property
    def price(self):
        return InstrumentServices(instrument=self).get_online_price()

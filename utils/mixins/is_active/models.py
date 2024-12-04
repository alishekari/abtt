from django.db import models

from utils.mixins.is_active.managers import IsActiveManager


class IsActiveMixin(models.Model):
    _is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    objects = IsActiveManager()

    @property
    def is_active(self):
        return self._is_active

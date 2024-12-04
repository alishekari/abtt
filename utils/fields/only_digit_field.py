from django.core import checks
from django.core.validators import RegexValidator
from django.db import models


class DigitField(models.CharField):
    def __init__(self, *args, min_length, **kwargs):
        self.min_length = min_length
        kwargs["validators"] = [
            RegexValidator(
                regex=r"^\d{{{min_length},{max_length}}}$".format(
                    min_length=self.min_length, max_length=kwargs["max_length"]
                )
            )
        ]
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_min_length_attribute(**kwargs),
        ]

    def _check_min_length_attribute(self, **kwargs):
        if self.min_length is None:
            return [
                checks.Error(
                    "OnlyDigitFields must define a 'min_length' attribute.",
                    obj=self,
                    id="fields.E120",
                )
            ]
        elif (
            not isinstance(self.min_length, int)
            or isinstance(self.min_length, bool)
            or self.min_length <= 0
        ):
            return [
                checks.Error(
                    "'min_length' must be a positive integer.",
                    obj=self,
                    id="fields.E121",
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["min_length"] = self.min_length
        del kwargs["validators"]
        return name, path, args, kwargs

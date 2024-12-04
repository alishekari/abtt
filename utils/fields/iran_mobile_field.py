import re

from django.core.validators import RegexValidator
from django.db import models
from rest_framework.fields import Field


class IranMobileField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [
            RegexValidator(
                regex=r"^09\d{9}$", message="Mobile should be like 09123456789", code="invalid_mobile"
            )
        ]
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
        ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        return name, path, args, kwargs


class SerializerIranMobileField(Field):
    default_error_messages = {
        'invalid_mobile': 'Mobile should be like 09123456789',
    }
    def to_internal_value(self, data):
        if not re.match("^09\d{9}$", data):
            self.fail("invalid_mobile")
        return data

    def to_representation(self, value):
        return value
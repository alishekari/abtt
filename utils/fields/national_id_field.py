from utils.fields.only_digit_field import DigitField


class NationalIdField(DigitField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 10
        kwargs["min_length"] = 10
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["min_length"]
        return name, path, args, kwargs

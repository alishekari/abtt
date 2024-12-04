from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StatementType(TextChoices):
    CREDIT = 'credit', _('بستانکار')
    DEBIT = 'debit', _('بدهکار')

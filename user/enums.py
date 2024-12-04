from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AdminGroups(TextChoices):
    SUPER_ADMIN = "super_admin", _("سوپر ادمین")
    SALES = "sales", _("فروش")
    SERVICE = "service", _("سرویس")
    CONTENT = "content", _("محتوا")


class ClientSex(TextChoices):
    MALE = "male", _("مرد")
    FEMALE = "female", _("زن")

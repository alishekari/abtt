from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class QATypes(TextChoices):
    ServiceCategory = 'شاخه خدمات'
    Service = 'خدمات'
    BlogPost = 'پست بلاگ'
    Page = 'صفحه ایستا'

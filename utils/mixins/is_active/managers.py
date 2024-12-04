from django.db import models


class IsActiveManager(models.Manager):
    def active_only(self):
        return self.get_queryset().filter(_is_active=True)

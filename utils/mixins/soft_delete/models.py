from django.db import models

from utils.mixins.soft_delete.managers import SoftDeleteManager


class SoftDeleteMixin(models.Model):
    _deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self._deleted_at = timezone.now()
        self.save(update_fields=['_deleted_at'])

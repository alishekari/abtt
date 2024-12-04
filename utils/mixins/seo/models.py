from django.contrib.postgres.fields import ArrayField
from django.db import models


class SeoMixin(models.Model):
    page_title = models.CharField(verbose_name='عنوان صفحه', max_length=512, blank=True, null=True)
    meta_description = models.CharField(verbose_name='توضیحات متا', max_length=256, blank=True, null=True)
    meta_title = models.CharField(verbose_name='عنوان متا', max_length=128, blank=True, null=True)
    meta_tags = ArrayField(models.CharField(max_length=128), blank=True, null=True)
    keywords = ArrayField(models.CharField(max_length=128), blank=True, null=True)
    canonical = models.URLField(blank=True, null=True)
    schema = models.JSONField(blank=True, null=True)
    nofollow = models.BooleanField(default=False)
    noindex = models.BooleanField(default=False)

    class Meta:
        abstract = True

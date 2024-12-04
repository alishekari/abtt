from django.contrib.auth.models import AbstractUser

from user.query_sets import CustomUserManager
from utils.fields.iran_mobile_field import IranMobileField
from utils.fields.national_id_field import NationalIdField


def get_thumbnail_image_path(instance, filename):
    return f"user_images/{instance.id}/{filename}"


class User(AbstractUser):
    national_id = NationalIdField(
        blank=True,
        null=True,
        unique=True,
        error_messages={"unique": "A user with that national id already exists."},
    )
    mobile = IranMobileField(
        blank=True,
        null=True,
        unique=True,
        error_messages={"unique": "A user with that mobile already exists."},
    )

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        ordering = ("-id",)

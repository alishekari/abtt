from django.db.models import Q

from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def search(self, query):
        from django.db.models.functions import Concat
        from django.db.models import Value

        return self.get_queryset().annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(national_id__icontains=query) |
            Q(mobile__icontains=query)
        )

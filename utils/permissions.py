from rest_framework import permissions

from user.enums import AdminGroups
from user.models import User, Admin


class SuperAdminPermission(permissions.IsAdminUser):
    """
    Global permission check for Super Admin.
    """

    def has_permission(self, request, view):
        try:
            admin: Admin = request.user.admin
            if admin.group == AdminGroups.SUPER_ADMIN and admin.is_active:
                return True
            return super().has_permission(request=request, view=view)
        except:
            return super().has_permission(request=request, view=view)


class EmployeePermission(permissions.IsAdminUser):
    """
    Global permission check for Employee.
    """

    def has_permission(self, request, view):
        try:
            user: User = request.user
            if hasattr(user, "employee"):
                return True
            return super().has_permission(request=request, view=view)
        except:
            return super().has_permission(request=request, view=view)


class EmployerPermission(permissions.IsAdminUser):
    """
    Global permission check for Employer.
    """

    def has_permission(self, request, view):
        try:
            user: User = request.user
            if hasattr(user, "employer"):
                return True
            return super().has_permission(request=request, view=view)
        except:
            return super().has_permission(request=request, view=view)

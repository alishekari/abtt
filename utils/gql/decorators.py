from functools import wraps

from django.core.exceptions import PermissionDenied
from graphql import GraphQLError

from user.enums import AdminGroups
from user.models import Admin, User


def super_admin_check_permission(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            user = args[1].context.user
            if user.is_superuser or user.admin.group == AdminGroups.SUPER_ADMIN:
                return function(*args, **kwargs)
            raise GraphQLError("You do not have permission to access this.")
        except:
            raise GraphQLError("You do not have permission to access this.")

    return wrapper


def is_authenticated_permission(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            user = args[1].context.user
            if user.is_authenticated:
                return function(*args, **kwargs)
            raise GraphQLError("You do not have permission to access this.")
        except:
            raise GraphQLError("You do not have permission to access this.")

    return wrapper


def is_employer_permission(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            employer = args[1].context.user.employer
            if employer.is_active:
                return function(*args, **kwargs)
            raise GraphQLError("You do not have permission to access this.")
        except:
            raise GraphQLError("You do not have permission to access this.")

    return wrapper

def is_employee_permission(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            employer = args[1].context.user.employee
            if employer.is_active:
                return function(*args, **kwargs)
            raise GraphQLError("You do not have permission to access this.")
        except:
            raise GraphQLError("You do not have permission to access this.")

    return wrapper

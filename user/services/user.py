from ..models import User, Admin


class UserServices:
    def __init__(self, user: User):
        self.user = user

    @staticmethod
    def get_or_create_by_mobile(mobile: str, name: str = None) -> User:
        user, created = User.objects.get_or_create(username=mobile, mobile=mobile)
        if name and created:
            user.first_name = name
            user.save(update_fields=['first_name'])
        return user

    @staticmethod
    def get_or_create_by_unique_data(
            mobile: str,
            username: str,
            national_id: str,
            birthdate=None,
            sex=None,
            first_name=None,
            last_name=None
    ) -> User:
        from django.db import IntegrityError
        try:
            user, created = User.objects.get_or_create(
                mobile=mobile,
                national_id=national_id,
                username=username
            )
        except IntegrityError:
            raise ValueError("User with this mobile or national id or username already exists.")
        return user

    @staticmethod
    def admin_authenticate(username: str, password: str) -> Admin:
        """
        Authenticates an client user by their username and password.

        Parameters:
            username (str): The username of the client user.
            password (str): The password of the client user.

        Returns:
            Admin: The authenticated client user or None if authentication failed.
        """
        username = username.strip().lower()
        password = password.strip()
        try:
            admin = Admin.objects.get(user__username=username)
            if admin.user.check_password(password):
                return admin
            else:
                raise Admin.DoesNotExist
        except Admin.DoesNotExist:
            return Admin.objects.none()

    @staticmethod
    def get_random_admin_id() -> int:
        """
        A static method to get a random client ID from the Admin objects.
        """
        return Admin.objects.all().order_by('?').first().id

from rest_framework import serializers

from user.models import User, Admin
from user.services.user import UserServices


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'username', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'mobile': {'required': True},
        }

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        mobile = data.get('mobile', None)
        if mobile:
            data['username'] = mobile

        return data


class LoginSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "login_failed": "Username or password is incorrect.",
    }

    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    refresh = serializers.CharField(required=False, read_only=True)
    access = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'refresh', 'access', 'username', 'password']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        from rest_framework_simplejwt.tokens import RefreshToken
        from user.services.user import UserServices

        admin = UserServices.admin_authenticate(validated_data['username'], validated_data['password'])
        if admin:
            user = admin.user
            refresh = RefreshToken.for_user(user)
            user.refresh = str(refresh)
            user.access = str(refresh.access_token)
            return user
        self.fail("login_failed")


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'national_id', 'mobile', 'birthdate', 'sex', 'thumbnail', 'email',
                  'password']
        extra_kwargs = {
            'mobile': {'required': True},
        }


class AdminCreateSerializer(serializers.ModelSerializer):
    user = UserWriteSerializer(required=True)

    class Meta:
        model = Admin
        fields = ['id', 'user', 'group']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserServices.get_or_create_by_unique_data(
            mobile=user_data['mobile'],
            username=user_data['mobile'],
            national_id=user_data.get('national_id', None)
        )
        user.first_name = user_data.get('first_name', None)
        user.last_name = user_data.get('last_name', None)
        user.set_password(raw_password=user_data['password'])
        user.save()
        admin = Admin.objects.create(user=user, **validated_data)
        return admin


class AdminEditSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=False)

    class Meta:
        model = Admin
        fields = ['group', '_is_active', 'password']

    def update(self, instance: Admin, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.user.set_password(password)
            instance.user.save(update_fields=['password'])
        return super().update(instance, validated_data)

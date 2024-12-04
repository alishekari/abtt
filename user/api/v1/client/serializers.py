from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.ModelSerializer):
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "refresh", "access", "sex"]

    def get_refresh(self, user: User):
        return self.context["refresh"]

    def get_access(self, user: User):
        return self.context["access"]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "national_id", "birthdate", "sex", "thumbnail", "email"]

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.api.v1.admin.serializers import UserSerializer, LoginSerializer, AdminCreateSerializer, AdminEditSerializer
from user.models import User, Admin
from utils.permissions import SuperAdminPermission


class UserViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):

    queryset = User.objects.all()

    serializer_action_classes = {
        "login": LoginSerializer,
        "create": UserSerializer,
        "partial_update": UserSerializer,
        "destroy": UserSerializer
    }

    permission_action_classes = {
        "login": [],
        "create": [SuperAdminPermission(),],
        "partial_update": [SuperAdminPermission(),],
        "destroy": [SuperAdminPermission(),]
    }

    queryset_action_classes = {
        "login": User.objects.all(),
        "create": User.objects.all(),
        "partial_update": User.objects.all(),
        "destroy": User.objects.all()
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def get_permissions(self):
        return self.permission_action_classes[self.action]

    @action(detail=False, url_path=r"login", methods=['post'], name='login')
    def login(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    queryset = Admin.objects.all()

    serializer_action_classes = {
        "create": AdminCreateSerializer,
        "partial_update": AdminEditSerializer,
    }

    permission_action_classes = {
        "create": [SuperAdminPermission(),],
        "partial_update": [SuperAdminPermission(),],
        "destroy": [SuperAdminPermission(),]
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    def get_permissions(self):
        return self.permission_action_classes[self.action]

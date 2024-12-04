from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from otp.services.otp_sms import OtpSmsServices
from user.api.v1.client.serializers import  UserWriteSerializer
from user.services.user import UserServices


class UserViewSet(GenericViewSet):

    serializer_action_classes = {
        "me": UserWriteSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    permission_action_classes = {
        "me": [IsAuthenticated()],
        "request_token": [],
        "verify_token": [],
    }

    def get_permissions(self):
        return self.permission_action_classes[self.action]

    def get_object(self):
        return self.request.user

    lookup_field = None

    @action(detail=False, url_path=r"request-token/(?P<mobile>09\d{9})", methods=['get'], name='request_token')
    def request_token(self, request, mobile):
        self.permission_classes = []
        user = UserServices.get_or_create_by_mobile(mobile=mobile)
        if OtpSmsServices.send_sms(user):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path=r"verify-token", methods=['post'], name='verify_token')
    def verify_token(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        from user.api.v1.client.serializers import LoginSerializer

        user = OtpSmsServices.check_token(mobile_number=request.data['mobile'], code=int(request.data['code']))
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = LoginSerializer(user, context={'refresh': str(refresh), 'access': str(refresh.access_token)})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="me", methods=['patch'], name='me')
    def me(self, request):
        serializer = self.get_serializer_class()(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

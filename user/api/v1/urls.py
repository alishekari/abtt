from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.api.v1.client.views import UserViewSet as ClientUserViewSet
from user.api.v1.admin.views import UserViewSet as AdminUserViewSet, AdminViewSet

router = DefaultRouter()
router.register(r"client", ClientUserViewSet, basename="user_client")
router.register(r"client/manage", AdminViewSet, basename="user_admin_management")
router.register(r"client", AdminUserViewSet, basename="user_admin")


urlpatterns = [
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

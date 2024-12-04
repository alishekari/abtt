from rest_framework.routers import DefaultRouter

from .client.views import OrderViewSet

router = DefaultRouter()
router.register(r"client", OrderViewSet, basename="order_user")

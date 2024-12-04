from django.urls import include, path

from .v1.urls import router

urlpatterns = [
    path("v1/", include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers

from network.views import ProfileViewSet, PostViewSet, LikeViewSet

app_name = "network"
router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

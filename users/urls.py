from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from users.apps import UsersConfig
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')


urlpatterns = [
              ] + router.urls
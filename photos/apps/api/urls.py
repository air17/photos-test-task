from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import PhotoViewSet, register, get_names

app_name = "api"

router = routers.SimpleRouter()
router.register("photos", PhotoViewSet, basename="photos")

urlpatterns = [
    path("names/", get_names, name="autofill"),
    path("register/", register, name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls

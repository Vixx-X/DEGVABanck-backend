
from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"payway-keys",
    views.PaywayKeysViewSet,
)


user_payway_key_urls = [
    path(
        "payway-keys/",
        views.UserPaywayKeysCreateView.as_view(),
        name="user-payway-key",
    ),
]

urlpatterns = [
    path(
        "user/",
        include(user_payway_key_urls),
    ),
    path(
        "",
        include(router.urls),
    ),
]

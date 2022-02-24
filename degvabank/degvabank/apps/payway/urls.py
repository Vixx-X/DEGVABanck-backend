
from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"payway-keys",
    views.PaywayKeysViewSet,
)
router.register(
    r"payway-meta",
    views.PaywayMetaViewSet,
)


user_payway_urls = [
    path(
        "payway-keys/",
        views.UserPaywayKeysCreateView.as_view(),
        name="user-payway-key",
    ),
    path(
        "payway-meta/",
        views.UserPayWayMetaListCreateView.as_view(),
        name="user-payway-meta",
    ),
]

urlpatterns = [
    path(
        "user/",
        include(user_payway_urls),
    ),
    path(
        "",
        include(router.urls),
    ),
]


from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"payway-keys",
    views.PayWayKeysViewSet,
)
router.register(
    r"payway-meta",
    views.PayWayMetaViewSet,
)
user_router = routers.DefaultRouter()
user_router.register(
    r"payway-meta",
    views.UserPayWayMetaViewSet,
)


user_payway_urls = [
    path(
        "payway-meta/<slug:app_id>/keys/",
        views.UserPayWayKeysCreateView.as_view(),
        name="user-payway-key",
    ),
    path(
        "",
        include(user_router.urls)
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

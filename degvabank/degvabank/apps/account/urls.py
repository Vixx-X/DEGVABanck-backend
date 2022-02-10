from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"accounts",
    views.AccountViewSet,
)

user_account_urls = [
    path(
        "accounts/",
        views.UserAccountListCreateView.as_view(),
        name="user-accounts",
    ),
    path(
        "accounts/<int:id>/",
        views.UserAccountView.as_view(),
        name="user-account-detail",
    )
]

urlpatterns = [
    path(
        "user/",
        include(user_account_urls),
    ),
    path(
        "",
        include(router.urls),
    ),
]

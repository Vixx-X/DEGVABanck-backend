from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"transactions",
    views.TransactionViewSet,
)

user_transaction_urls = [
    path(
        "transactions/",
        views.UserTransactionListCreateView.as_view(),
        name="user-transactions",
    ),
    path(
        "transactions/<int:id>/",
        views.UserTransactionView.as_view(),
        name="user-transactions-detail",
    ),
]

urlpatterns = [
    path(
        "user/",
        include(user_transaction_urls),
    ),
    path(
        "",
        include(router.urls),
    ),
]

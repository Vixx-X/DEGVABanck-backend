from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"credit-cards",
    views.CreditCardViewSet,
)
router.register(
    r"debit-cards",
    views.DebitCardViewSet,
)

credit_card_urls = [
    path(
        "credit-cards/",
        views.UserCreditCardListCreateView.as_view(),
        name="user-credit-cards",
    ),
    path(
        "credit-cards/<int:id>/",
        views.UserCreditCardView.as_view(),
        name="user-credit-card-detail",
    ),
]

debit_card_urls = [
    path(
        "debit-cards/",
        views.UserDebitCardListCreateView.as_view(),
        name="user-credit-cards",
    ),
    path(
        "debit-cards/<int:id>/",
        views.UserDebitCardView.as_view(),
        name="user-debit-card-detail",
    ),
]

urlpatterns = [
    path(
        "user/",
        include(credit_card_urls),
    ),
    path(
        "user/",
        include(debit_card_urls),
    ),
    path(
        "",
        include(router.urls),
    ),
]

from django.urls.conf import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    r"petitions",
    views.PetitionViewSet,
)

user_transaction_urls = [
    path(
        "petitions/",
        views.UserPetitionListView.as_view(),
        name="user-petitions",
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

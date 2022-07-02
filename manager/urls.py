from django.urls import path

from .views import (
    RegisterApiView,
    LoginView,
    LogoutView,
    EditTeamView,
    PlayerInfoUpdateView,
    SetPlayerOnTransferView,
    TransferMarketList
)


urlpatterns = [
    path("auth/register/", RegisterApiView.as_view(), name="api-register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("team/edit/", EditTeamView.as_view(), name="edit"),
    path(
        "player/<int:pk>/",
        PlayerInfoUpdateView.as_view(),
        name="edit-player",
    ),
    path(
        "add-to-market/player/<int:pk>/",
        SetPlayerOnTransferView.as_view(),
        name="add-to-market",
    ),
    path("transfer-market/", TransferMarketList.as_view(), name="transfer_market"),
]

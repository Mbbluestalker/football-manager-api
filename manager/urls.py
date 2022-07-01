from django.urls import path

from .views import RegisterApiView, LoginView, LogoutView
                    


urlpatterns = [
    path("auth/register/", RegisterApiView.as_view(), name="api-register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

]
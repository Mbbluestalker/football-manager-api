from django.urls import path

from .views import RegisterApiView, LoginView
                    


urlpatterns = [
    path("auth/register/", RegisterApiView.as_view(), name="api-register"),
    path("auth/login/", LoginView.as_view(), name="login"),
]
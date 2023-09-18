from django.urls import path
from .views import api_home, UserCreateView, create_user


urlpatterns = [
    path("", api_home),
    path("auth/register", UserCreateView.as_view()),
    path("test/register", create_user),
]

from django.urls import path
from .views import api_home, UserCreateView


urlpatterns = [path("", api_home), path("auth/register", UserCreateView.as_view())]

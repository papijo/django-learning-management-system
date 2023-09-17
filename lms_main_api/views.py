from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins, permissions

from .serializers import UserSerializer

from main.models import User

# Create your views here.


@api_view(["GET"])  # Only Allowed HTTP Method
def api_home(request, *args, **kwargs):
    """Learning Management System API Home Route"""

    application_information = {
        "Application Name": "Learning Management System REST Web and Mobile Server API",
        "Application Owner": "Ebhota Jonathan, Abuja Nigeria",
        "Application Version": "1.0.0",
        "Application Engineer": "Ebhota Jonathan",
    }

    return Response(application_information)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

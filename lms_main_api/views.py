from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, mixins, permissions, status

from .utils.serializers import UserSerializer

from main.models import User

# Create your views here.


@api_view(["GET"])  # Only Allowed HTTP Method
def api_home(request, *args, **kwargs):
    """Learning Management System API Home Route"""

    application_information = {
        "Application Name": "Learning Management System: Web and Mobile REST API Server",
        "Application Owner": "Ebhota Jonathan, Abuja Nigeria",
        "Application Version": "1.0.0",
        "Application Engineer": "Ebhota Jonathan",
    }

    return Response(application_information)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def create_user(request):
    if request.method == "POST":
        data = request.data

        # Perform additional validation here
        if not data.get("first_name"):
            return Response(
                {"error": "First name is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res = {"message": "User created successfully"}
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

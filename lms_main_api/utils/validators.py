from rest_framework import serializers


from main.models import User


def validate_first_name(value):
    if not value:
        raise serializers.ValidationError("Field cannot be empty")
    return value

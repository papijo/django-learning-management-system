from rest_framework import serializers

from main.models import User
from .validators import validate_first_name


# class UserSerializer(serializers.ModelSerializer):
#     password_confirm = serializers.CharField(write_only=True)
#     first_name = serializers.CharField(
#         # error_messages={
#         #     "blank": "Field cannot be empty.",
#         # },
#         validators=[validate_first_name],
#     )

#     class Meta:
#         model = User
#         fields = ("email", "password", "password_confirm", "first_name", "last_name")

#     def validate(self, data):
#         print(data)
#         password = data.get("password")
#         password_confirm = data.get("password_confirm")

#         if password != password_confirm:
#             raise serializers.ValidationError({"error": "Passwords do not match"})

#         return data

#     def create(self, validated_data):
#         password = validated_data.pop("password")
#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "first_name", "last_name")

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")  # Remove 'password_confirm' field
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

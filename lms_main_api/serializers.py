from rest_framework import serializers

from main.models import User


# serializers.py
class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "password_confirm", "first_name", "last_name")

    def create(self, validated_data):
        password = validated_data.pop("password")
        password_confirm = validated_data.pop("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

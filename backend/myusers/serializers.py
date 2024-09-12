from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "first_name", "last_name", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            print(serializers.ValidationError())
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data["first_name"] = (
            validated_data.get("first_name", "").strip().capitalize()
        )
        validated_data["last_name"] = (
            validated_data.get("last_name", "").strip().capitalize()
        )

        validated_data["email"] = validated_data.get("email", "").strip()

        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

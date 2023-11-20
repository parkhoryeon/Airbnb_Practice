from rest_framework import serializers
from .models import User


""" User 최소 정보 """
class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


""" User 상세 정보(Private) """
class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
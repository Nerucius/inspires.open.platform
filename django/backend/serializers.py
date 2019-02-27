from rest_framework import serializers
from backend import models

from backend.serializers_base import *


class UserSerializer(serializers.ModelSerializer):
    groups = SimpleGroupSerializer(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = [
            "pk",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar_url",
            "groups",
        ]

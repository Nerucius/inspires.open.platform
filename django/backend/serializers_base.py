from rest_framework import serializers
from backend import models


# Serializers define the API representation.
class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Group
        fields = ["pk", "name"]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["pk", "username", "first_name", "last_name", "email", "avatar_url"]

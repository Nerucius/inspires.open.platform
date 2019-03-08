from rest_framework import serializers
from backend import models


class TrackableModelSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=models.User.objects)

    # def get_field_names(self, declared_fields, info):
    #     print("get_field_names")
    #     fields = super(TrackableModelSerializer, self).get_field_names(
    #         declared_fields, info
    #     )
    #     fields += ["created_by", "created_at", "modified_by", "modified_at", "owner"]
    #     return fields


# Serializers define the API representation.
class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Group
        fields = ["pk", "name"]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["pk", "username", "first_name", "last_name", "avatar_url"]


class CollaborationSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects)
    structure = serializers.PrimaryKeyRelatedField(queryset=models.Structure.objects)
    partners = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Project.objects
    )

    class Meta:
        model = models.Collaboration
        fields = ["pk", "is_approved", "project", "structure", "partners"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["pk", "name", "managers"]


class SimpleStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Structure
        fields = ["pk", "name"]


class SimpleKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ["pk", "name"]

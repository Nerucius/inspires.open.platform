from rest_framework import serializers
from backend import models

from backend.serializers_base import *


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    managed_projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    researched_projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    managed_structures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owned_structures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "avatar_url",
            "groups",
            "owned_projects",
            "managed_projects",
            "researched_projects",
            "managed_structures",
            "owned_structures",
        ]


class ProjectSerializer(TrackableModelSerializer):
    collaboration = CollaborationSerializer(read_only=True)
    participants = ParticipationSerializer(
        source="participation_set", many=True, read_only=True
    )
    phases = ProjectAtPhaseSerializer(
        source="projectatphase_set", many=True, read_only=True
    )
    managers = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=models.User.objects
    )
    keywords = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=models.Keyword.objects
    )

    class Meta:
        model = models.Project
        fields = "__all__"
        # fields = ["collaboration", "participants", "managers", "keywords"]


class StructureSerializer(TrackableModelSerializer):
    managers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects
    )
    validation = serializers.PrimaryKeyRelatedField(read_only=True)
    collaborations = CollaborationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Structure
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Keyword
        fields = ["id", "name", "projects"]

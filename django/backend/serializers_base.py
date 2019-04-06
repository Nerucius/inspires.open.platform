from rest_framework import serializers
from backend import models


class TrackableModelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        required=False, queryset=models.User.objects
    )
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)


class SimpleGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Group
        fields = ["id", "name"]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "avatar_url",
        ]


class CollaborationSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects)
    structure = serializers.PrimaryKeyRelatedField(queryset=models.Structure.objects)
    partners = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=models.Project.objects
    )

    class Meta:
        model = models.Collaboration
        fields = ["id", "is_approved", "project", "structure", "partners"]


class ProjectPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectPhase
        fields = "__all__"


class ProjectAtPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectAtPhase
        fields = "__all__"


class ProjectAtPhaseSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects)
    project_phase = serializers.PrimaryKeyRelatedField(
        queryset=models.ProjectPhase.objects
    )

    class Meta:
        model = models.ProjectAtPhase
        fields = "__all__"


class ParticipationSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects)
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects)
    role = serializers.PrimaryKeyRelatedField(queryset=models.ParticipationRole.objects)

    class Meta:
        model = models.Participation
        fields = ["id", "user", "project", "role"]


class SimpleKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ["id", "name"]


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KnowledgeArea
        fields = ["id", "code", "name"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    knowledge_area = KnowledgeAreaSerializer()

    class Meta:
        model = models.Project
        fields = [
            "id",
            "name",
            "participants",
            "keywords",
            "summary",
            "image_url",
            "knowledge_area",
        ]


class SimpleStructureSerializer(serializers.ModelSerializer):
    knowledge_areas = KnowledgeAreaSerializer(many=True)

    class Meta:
        model = models.Structure
        fields = [
            "id",
            "name",
            "summary",
            "image_url",
            "year_founded",
            "knowledge_areas",
        ]

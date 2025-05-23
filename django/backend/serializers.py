from rest_framework import serializers
from backend import models

from backend.serializers_base import *


class UserSerializer(serializers.ModelSerializer):
    # groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    managed_projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    researched_projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    managed_structures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owned_structures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    first_name = serializers.CharField(source="first_name_anon", read_only=True)
    last_name = serializers.CharField(source="last_name_anon", read_only=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            # "email",
            "avatar_url",
            "gender",
            "institution",
            "education_level",
            "owned_projects",
            "managed_projects",
            "researched_projects",
            "managed_structures",
            "owned_structures",
            "is_administrator",
            "is_superuser",
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
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
            "hide_realname",
            "avatar_url",
            "gender",
            "institution",
            "education_level",
            "owned_projects",
            "managed_projects",
            "researched_projects",
            "managed_structures",
            "owned_structures",
            "is_staff",
            "is_editor",
            "is_superuser",
            "is_administrator",
        ]


class ProjectSerializer(AttachmentFieldMixin, TrackableModelSerializer):
    eval_version = serializers.IntegerField(read_only=True)
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
    attachments = serializers.SerializerMethodField(method_name="get_attachments")

    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectEvaluationsSerializer(TrackableModelSerializer):
    evaluations = EvaluationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = ["evaluations"]


class ProjectStatsSerializer(TrackableModelSerializer):
    statN = serializers.IntegerField()
    statPhases = serializers.CharField()

    class Meta:
        model = models.Project
        fields = ["statN", "statPhases"]


class StructureSerializer(AttachmentFieldMixin, TrackableModelSerializer):
    managers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects
    )
    validation = serializers.PrimaryKeyRelatedField(read_only=True)
    collaborations = CollaborationSerializer(many=True, read_only=True)
    networks = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=models.Network.objects
    )
    attachments = serializers.SerializerMethodField(method_name="get_attachments")

    class Meta:
        model = models.Structure
        fields = "__all__"


class KeywordSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Keyword
        fields = ["id", "name", "projects"]


class EvaluationQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Evaluation
        fields = ["questions"]


class EvaluationResponsesSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(source="response_set", many=True, read_only=True)

    class Meta:
        model = models.Evaluation
        fields = ["responses"]

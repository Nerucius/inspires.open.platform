from rest_framework import serializers
from backend import models
from django.contrib.contenttypes.models import ContentType


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

    first_name = serializers.CharField(source="first_name_anon", read_only=True)
    last_name = serializers.CharField(source="last_name_anon", read_only=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "avatar_url",
            "groups",
            "is_superuser",
            "is_administrator",
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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = "__all__"


class SimpleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ["id", "i18n", "answer_type", "answer_range", "answers"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
    project = serializers.IntegerField(source="project_pk", read_only=True)
    answer_type = serializers.CharField(read_only=True)

    class Meta:
        model = models.Response
        fields = "__all__"


class SimpleKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ["id", "name"]


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KnowledgeArea
        fields = ["id", "code", "name"]


class SimpleStructureSerializer(serializers.ModelSerializer):
    knowledge_areas = KnowledgeAreaSerializer(many=True)

    class Meta:
        model = models.Structure
        fields = [
            "id",
            "created_by",
            "name",
            "summary",
            "image_url",
            "year_founded",
            "knowledge_areas",
            "collaborations",
            "modified_at",
        ]


class StructureValidationSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.StructureValidation
        fields = ["id", "structure", "created_by", "is_approved"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    class ProjectStructureSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Structure
            fields = ["id", "name"]

    knowledge_area = KnowledgeAreaSerializer()
    structure = ProjectStructureSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = [
            "id",
            "modified_at",
            "name",
            "participants",
            "keywords",
            "summary",
            "country_code",
            "image_url",
            "knowledge_area",
            "project_type",
            "structure",
        ]


class EvaluationSerializer(serializers.ModelSerializer):
    # project = SimpleProjectSerializer(read_only=True)
    # project_phase = ProjectPhaseSerializer(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)
    project = serializers.IntegerField(
        source="participation.project.pk", read_only=True
    )
    role = serializers.IntegerField(source="participation.role.pk", read_only=True)
    project_phase = serializers.IntegerField(source="project_phase.pk", read_only=True)
    user = serializers.IntegerField(source="participation.user.id", read_only=True)
    user_eval_token = serializers.CharField(
        source="participation.user.eval_token", read_only=True
    )

    class Meta:
        model = models.Evaluation
        fields = "__all__"


class SimpleAttachmentSerializer(TrackableModelSerializer):
    class Meta:
        model = models.Attachment
        fields = ["id", "name", "size", "url"]


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class AttachmentSerializer(TrackableModelSerializer):
    class Meta:
        model = models.Attachment
        fields = "__all__"


class ContentMasterSerializer(TrackableModelSerializer):
    class Meta:
        model = models.ContentMaster
        fields = ["id", "type", "name"]


class SimpleContentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)
    sorting = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Content
        fields = [
            "master",
            "sorting",
            "type",
            "title",
            "topic",
            "summary",
            "slug",
            "locale",
            "published",
        ]


class ContentSerializer(TrackableModelSerializer):
    attachments = AttachmentSerializer(read_only=True, many=True)
    sorting = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Content
        fields = "__all__"
        lookup_field = "slug"

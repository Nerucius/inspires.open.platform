from rest_framework import serializers
from backend import models


class TrackableModelSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(
        required=False, queryset=models.User.objects
    )

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


class ParticipationSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=models.Project.objects)
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects)
    role = serializers.PrimaryKeyRelatedField(queryset=models.ParticipationRole.objects)

    class Meta:
        model = models.Participation
        fields = ["id", "user", "project", "role"]


class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["id", "name", "participants", "keywords", "summary", "image_url"]


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
            "name",
            "summary",
            "image_url",
            "year_founded",
            "knowledge_areas",
        ]

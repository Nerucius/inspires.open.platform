from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from backend import models

READONLY_FIELDS = ["password", "created_at", "created_by", "modified_at", "modified_by", "slug"]
LIST_HIDDEN_FIELDS = [
    "password",
    "created_at",
    "created_by",
    "modified_at",
    "modified_by",
    "description",
    "body",
]


def column_lister(model):
    """ Creates a new ModelAdmin that always lists the models in a table fashion. """

    class ListAdmin(admin.ModelAdmin):
        readonly_fields = [
            f.name for f in model._meta.fields if f.name in READONLY_FIELDS
        ]
        list_display = [
            f.name for f in model._meta.fields if f.name not in LIST_HIDDEN_FIELDS
        ]

    return ListAdmin


# Create admin views

admin.site.register(models.User, UserAdmin)

for model in [
    Permission,
    LogEntry,
    ContentType,
    models.Structure,
    models.StructureValidation,
    models.Collaboration,
    models.Network,
    models.Project,
    models.ProjectPhase,
    models.ProjectAtPhase,
    models.Participation,
    models.ParticipationRole,
    models.KnowledgeArea,
    models.ContentMaster,
    models.Content,
    models.Keyword,
    models.Evaluation,
    models.Question,
    models.Answer,
    models.Response,
]:
    admin.site.register(model, column_lister(model))

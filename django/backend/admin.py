from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType

from backend import models

HIDDEN_FIELDS = ["password", "created_at", "modified_at", "modified_by"]


def column_lister(model):
    """ Creates a new ModelAdmin that always lists the models in a table fashion. """

    class ListAdmin(admin.ModelAdmin):
        list_display = [
            f.name for f in model._meta.fields if f.name not in HIDDEN_FIELDS
        ]

    return ListAdmin


# Create admin views

admin.site.register(models.User, UserAdmin)

for model in [ContentType]:
    admin.site.register(model, column_lister(model))

from backend.models.project import Project
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from backend.models import TrackableModel


class Attachment(TrackableModel):
    name = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=128)
    size = models.PositiveIntegerField(default=0)
    url = models.URLField()

    # Generic relation to any object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name

    @classmethod
    def can_create(cls, user, data):
        content_type = data["content_type"]
        object_id = data["object_id"]

        # Max of 5 attachments per project
        # TODO: TEST THIS
        project_ct = ContentType.objects.get_for_model(Project)

        if content_type == project_ct:
            project = Project.objects.get(pk=object_id)
            return project.can_write(user)
        #     attch_count = Attachment.objects.filter(
        #         content_type=content_type, object_id=object_id
        #     ).count()
        #     if attch_count > 5:
        #         return False

        return True

    class Meta:
        ordering = ["id"]

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from backend.models import TrackableModel


# Create your models here.

# TODO: Finish attachment model
class Attachment(TrackableModel):
    name = models.CharField(max_length=255)
    url = models.URLField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name

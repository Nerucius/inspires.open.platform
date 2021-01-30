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

        
    class Meta:
        ordering = ["id"]

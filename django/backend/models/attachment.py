from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from backend.models import TrackableModel

MIME_TYPES = [
    ('image/png', 'Image (PNG)'),
    ('image/jpeg', 'Image (JPG)'),
    ('application/pdf', 'PDF File'),
]

class Attachment(TrackableModel):
    name = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=128, choices=MIME_TYPES)
    url = models.URLField()

    # Generic relation to any object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name


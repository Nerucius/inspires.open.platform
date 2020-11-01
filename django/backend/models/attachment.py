from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from backend.models import TrackableModel


# class Attachment(TrackableModel):
#     url = models.URLField()
#     name = models.CharField(max_length=512)
#     # extension = models.CharField(max_length=128)
#     mime_type = models.CharField(max_length=128)

#     # Generic relation to any object
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     target = GenericForeignKey("content_type", "object_id")

#     def __str__(self):
#         return self.name


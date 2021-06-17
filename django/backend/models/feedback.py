from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Feedback(models.Model):
    feedback_type = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    rating = models.IntegerField(blank=True, null=True)

    # Fields for tracking
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, null=True, editable=False)

    # Fields to point to object being affected
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "Feedback (%s) on %s [%i]" % (
            self.feedback_type,
            self.content_type.name,
            self.rating,
        )

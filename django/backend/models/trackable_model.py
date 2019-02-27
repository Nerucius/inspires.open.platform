import os, inspect

from django.db import models
from django.dispatch import receiver
from django.conf import settings

from hashlib import md5


class TrackableModel(models.Model):
    """ Base abstract model for all other models, adds tracking capabilities to the
        database and allows for more complex permissions.
    """

    is_trackable = True
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        editable=False,
        blank=True,
        null=True,
        related_name="created_%(class)s",
        related_query_name="created_%(class)ss",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
        related_name="modified_%(class)s",
        related_query_name="modified_%(class)ss",
    )
    modified_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owned_%(class)s",
        related_query_name="owned_%(class)ss",
        help_text="Owner of the instance. This user will be able to edit the\
            instance or even delete it.",
    )

    @classmethod
    def can_create(cls, user, data):
        return True

    def can_read(self, user):
        return True

    def can_write(self, user):
        return False

    class Meta:
        abstract = True


def get_current_request_user():
    """ Hack the python stack to find the request user. """
    user = None
    for entry in reversed(inspect.stack()):
        if "request" in entry[0].f_locals:
            try:
                user = entry[0].f_locals["request"].user
                break
            except:
                continue
    return user


@receiver(models.signals.pre_save)
def update_trackable(sender, instance, raw, using, update_fields, **kwargs):
    is_trackable = hasattr(sender, "is_trackable")
    if is_trackable:
        request_user = get_current_request_user()
        print("Tracked model %s by %s" % (sender, request_user.username))

        # If we are editing a user, set the owner to itself
        if sender.__name__ == "User":
            instance.owner = instance
        # Update created_by and modified_by
        if not instance.created_by:
            instance.created_by = request_user
        else:
            instance.modified_by = request_user

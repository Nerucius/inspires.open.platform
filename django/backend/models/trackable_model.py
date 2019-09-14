import os, inspect

from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

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
        related_name="created_%(class)ss",
        related_query_name="created_%(class)s",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
        related_name="modified_%(class)ss",
        related_query_name="modified_%(class)s",
    )
    modified_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="owned_%(class)ss",
        related_query_name="owned_%(class)s",
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
    for entry in reversed(inspect.stack()):
        if "request" in entry[0].f_locals:
            try:
                user = entry[0].f_locals["request"].user
                return user
            except:
                continue
    return None


@receiver(models.signals.pre_delete)
def delete_trackable(sender, instance, using, **kwargs):
    is_trackable = hasattr(sender, "is_trackable")
    if is_trackable:

        request_user = get_current_request_user()
        if not request_user or isinstance(request_user, AnonymousUser):
            return

        LogEntry.objects.log_action(
            user_id=request_user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=DELETION,
            change_message="TrackableModel Deleted",
        )


@receiver(models.signals.pre_save)
def update_trackable(sender, instance, raw, using, update_fields, **kwargs):
    is_trackable = hasattr(sender, "is_trackable")
    if is_trackable and not raw:

        request_user = get_current_request_user()
        if not request_user or isinstance(request_user, AnonymousUser):
            return

        if settings.DEBUG:
            print("Tracked model %s by %s" % (sender, request_user.username))

        # If we are editing a user, set the owner to itself
        if sender.__name__ == "User":
            instance.owner = instance
        # Update created_by and modified_by
        if not instance.created_by:
            instance.created_by = request_user
            instance.owner = request_user
        else:
            instance.modified_by = request_user


@receiver(models.signals.post_save)
def save_trackable(sender, instance, created, raw, using, update_fields, **kwargs):
    is_trackable = hasattr(sender, "is_trackable")

    if is_trackable and not raw:

        request_user = get_current_request_user()
        if not request_user or isinstance(request_user, AnonymousUser):
            return

        # Log Action
        LogEntry.objects.log_action(
            user_id=request_user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=(ADDITION if created else CHANGE),
            change_message="TrackableModel %s" % ("Created" if created else "Changed"),
        )

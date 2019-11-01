from django.db import models
from django.dispatch import receiver

from backend.models import TrackableModel, Project


class Collaboration(TrackableModel):

    is_approved = models.BooleanField(default=False)

    project = models.OneToOneField(
        "Project",
        on_delete=models.CASCADE,
        related_name="collaboration",
        related_query_name="collaboration",
    )
    structure = models.ForeignKey(
        "Structure",
        on_delete=models.CASCADE,
        related_name="collaborations",
        related_query_name="collaboration",
    )
    partners = models.ManyToManyField(
        "Structure",
        blank=True,
        related_name="partnerships",
        related_query_name="partnership",
    )

    @classmethod
    def can_create(cls, user, data):
        # Check performed by framework
        if len(data) == 0:
            return True

        # Can only create in a state of not approved and when user has write perm
        # to the project
        project = Project.objects.get(pk=data["project"])

        return (not hasattr(data, "is_approved")) and project.can_write(user)

    def can_write(self, user):
        # Only structure may change the instance
        return self.owner == user or self.structure.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return "Collab %s <-> %s" % (self.structure.name, self.project.name)


@receiver(models.signals.post_save)
def email_new_collaboration(
    sender, instance, raw, created, using, update_fields, **kwargs
):
    if created and isinstance(instance, Collaboration):
        from backend import email

        email.email_new_collaboration(instance)
        print("Sent email for new collaboration")


@receiver(models.signals.post_save)
def email_collaboration_approved(
    sender, instance, raw, created, using, update_fields, **kwargs
):
    if not created and isinstance(instance, Collaboration) and instance.is_approved:
        from backend import email

        email.email_collaboration_approved(instance)
        print("Sent email for collaboration approved")

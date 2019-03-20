from django.db import models

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
        return self.structure.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return "Collab %s <-> %s" % (self.structure.name, self.project.name)

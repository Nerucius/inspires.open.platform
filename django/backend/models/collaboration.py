from django.db import models

from backend.models import TrackableModel


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

    def can_write(self, user):
        return self.structure.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return "Collab %s <-> %s" % (self.structure.name, self.project.name)

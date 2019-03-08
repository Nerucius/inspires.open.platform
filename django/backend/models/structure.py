from django.db import models

from backend.models import TrackableModel, User


class Structure(TrackableModel):

    managers = models.ManyToManyField(
        User,
        blank=True,
        related_name="managed_structures",
        related_query_name="managed_structure",
    )

    name = models.CharField(max_length=254)

    def can_write(self, user):
        return self.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return self.name

from django.db import models

from backend.models import TrackableModel, User


class Project(TrackableModel):

    managers = models.ManyToManyField(
        User,
        blank=True,
        related_name="managed_projects",
        related_query_name="managed_project",
    )
    researchers = models.ManyToManyField(
        User,
        blank=True,
        related_name="researched_projects",
        related_query_name="researched_project",
    )

    keywords = models.ManyToManyField(
        "Keyword", blank=True, related_name="projects", related_query_name="project"
    )

    name = models.CharField(max_length=254)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=1024, blank=True)

    def can_write(self, user):
        return self.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return self.name

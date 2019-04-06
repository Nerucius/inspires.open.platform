from django.db import models

from backend.models import TrackableModel


class Project(TrackableModel):

    TYPE_RESEARCH = "research"
    TYPE_PUBLIC_ENGAGEMENT = "publicEngagement"
    TYPE_SERVICE_LEARNING = "serviceLearning"

    TYPES = [
        (TYPE_RESEARCH, "Research"),
        (TYPE_PUBLIC_ENGAGEMENT, "Public Engagement"),
        (TYPE_SERVICE_LEARNING, "Service Learning"),
    ]

    managers = models.ManyToManyField(
        "User",
        blank=True,
        related_name="managed_projects",
        related_query_name="managed_project",
    )
    participants = models.ManyToManyField(
        "User",
        through="Participation",
        blank=True,
        related_name="researched_projects",
        related_query_name="researched_project",
    )

    keywords = models.ManyToManyField(
        "Keyword", blank=True, related_name="projects", related_query_name="project"
    )

    acronym = models.CharField(max_length=32)
    name = models.CharField(max_length=254)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)

    image_url = models.URLField(max_length=500, blank=True)
    contact_email = models.EmailField(max_length=500, blank=True)
    contact_website = models.URLField(max_length=500, blank=True)

    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    project_type = models.CharField(max_length=64, blank=True, choices=TYPES)
    phases = models.ManyToManyField(
        "ProjectPhase", through="ProjectAtPhase", blank=True
    )

    # UNESCO Knowledge Area
    knowledge_area = models.ForeignKey(
        "KnowledgeArea", blank=True, null=True, on_delete=models.SET_NULL
    )

    # TODO: RequestForResearch
    # request = models.ForeignKey("RequestForReseach", null=True, blank=True, on_delete=models.SET_NULL)

    # TODO: Related to Evaluation
    # stage = models.ForeignKey("Stage", null=True, on_delete=models.SET_NULL)

    related_projects = models.ManyToManyField("Project", blank=True)

    def can_write(self, user):
        return self.managers.filter(pk=user.pk).exists() or user == self.owner

    def __str__(self):
        return self.name


class ProjectPhase(models.Model):
    order = models.SmallIntegerField()
    name = models.CharField(max_length=254)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class ProjectAtPhase(models.Model):
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    project_phase = models.ForeignKey("ProjectPhase", on_delete=models.CASCADE)

    def can_create(self, user, data):
        project = Project.objects.get(pk=data["project"])
        return self.project.can_write(user)

    def can_write(self, user):
        return self.project.can_write(user)

    class Meta:
        unique_together = ("project", "project_phase")


class Participation(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.ForeignKey("ParticipationRole", on_delete=models.CASCADE)

    def __str__(self):
        return "%s <-> %s" % (self.user.username, self.project.name)

    def can_create(self, user, data):
        project = Project.objects.get(pk=data["project"])
        return self.project.can_write(user)

    def can_write(self, user):
        return self.project.can_write(user)

    class Meta:
        unique_together = ("user", "project")


class ParticipationRole(models.Model):
    # SCI
    # STU
    # CSM

    tag = models.CharField(max_length=3)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

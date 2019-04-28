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
        through_fields=("project", "user"),
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
    contact_postal_address = models.TextField(blank=True)
    contact_social_facebook = models.URLField(max_length=500, blank=True)
    contact_social_twitter = models.URLField(max_length=500, blank=True)
    contact_social_other = models.URLField(max_length=500, blank=True)

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

    @property
    def evaluations(self):
        phases = ProjectAtPhase.objects.filter(project__pk=self.pk)
        evaluations = []
        for phase in phases:
            evaluations += phase.evaluation_set.all()
        return evaluations

    @property
    def structure(self):
        if hasattr(self, "collaboration"):
            return self.collaboration.structure
        return None

    def can_write(self, user):
        return self.managers.filter(pk=user.pk).exists() or user == self.owner

    def __str__(self):
        return self.name


class ProjectPhase(models.Model):
    order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=254)
    tag = models.CharField(max_length=50)

    def __str__(self):
        if "1" in self.name:
            return "Phase 1"
        if "2" in self.name:
            return "Phase 2"
        if "3" in self.name:
            return "Phase 3"
        if "4" in self.name:
            return "Phase 4"
        return self.name

    class Meta:
        ordering = ["order"]


class ProjectAtPhase(TrackableModel):
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    project_phase = models.ForeignKey("ProjectPhase", on_delete=models.CASCADE)

    def __str__(self):
        return "%s at %s" % (self.project.acronym, self.project_phase)

    @classmethod
    def can_create(cls, user, data):
        project = Project.objects.get(pk=data["project"])
        return project.can_write(user)

    def can_write(self, user):
        return self.project.can_write(user)

    class Meta:
        unique_together = ("project", "project_phase")


class Participation(TrackableModel):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.ForeignKey("ParticipationRole", on_delete=models.CASCADE)

    def __str__(self):
        return "[%s] %s as %s" % (self.project.acronym, self.user.username, self.role)

    @classmethod
    def can_create(cls, user, data):
        project = Project.objects.get(pk=data["project"])
        return project.can_write(user)

    def can_write(self, user):
        return self.project.can_write(user)

    class Meta:
        unique_together = ("user", "project")


class ParticipationRole(models.Model):
    tag = models.CharField(max_length=3)
    name = models.CharField(max_length=254)

    def __str__(self):
        if "scientist" in self.name:
            return "Scientist"
        if "student" in self.name:
            return "Student"
        if "civilSociety" in self.name:
            return "Civil Society"
        if "projectManager" in self.name:
            return "Project Manager"
        return self.name

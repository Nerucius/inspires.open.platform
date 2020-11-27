from django.db import models

from backend.models import TrackableModel, User

DEFAULT_DESCRIPTION = """## Background

(Explain your project's backstory and motivations)

## Objective

(What is the mission of your Project?)

## Method

(How is / was your project executed?)

## Results and discussion

(Write about what your project has found)

## Conclusion

(What have you learned?)
"""


class Project(TrackableModel):

    TYPE_RESEARCH = "RESEARCH"
    TYPE_PARTICIPATORY_RESEARCH = "PARTICIPATORY_RESEARCH"
    TYPE_PARTICIPATORY_ACTION_RESEARCH = "PARTICIPATORY_ACTION_RESEARCH"
    TYPE_CITIZEN_SCIENCE = "CITIZEN_SCIENCE"
    TYPE_PUBLIC_ENGAGEMENT = "PUBLIC_ENGAGEMENT"
    TYPE_SERVICE_LEARNING = "SERVICE_LEARNING"
    TYPE_ADVOCACY = "ADVOCACY"
    TYPE_INNOVATION = "INNOVATION"
    TYPE_POLICY_INNOVATION = "POLICY_INNOVATION"
    TYPE_OTHER = "OTHER"

    TYPES = [
        (TYPE_RESEARCH, "Research"),
        (TYPE_PARTICIPATORY_RESEARCH, "Participatory Research"),
        (TYPE_PARTICIPATORY_ACTION_RESEARCH, "Participatory Action Research"),
        (TYPE_CITIZEN_SCIENCE, "Citizen Science"),
        (TYPE_PUBLIC_ENGAGEMENT, "Public Engagement"),
        (TYPE_SERVICE_LEARNING, "Service Learning"),
        (TYPE_ADVOCACY, "Advocacy"),
        (TYPE_INNOVATION, "Innovation"),
        (TYPE_POLICY_INNOVATION, "Policy Innovation"),
        (TYPE_OTHER, "Other"),
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
    description = models.TextField(blank=True, default=DEFAULT_DESCRIPTION)
    country_code = models.CharField(max_length=16, blank=True)

    image_url = models.URLField(max_length=500, blank=True)

    contact_email = models.EmailField(max_length=500, blank=True)
    contact_website = models.URLField(max_length=500, blank=True)
    contact_postal_address = models.TextField(blank=True)
    contact_social_facebook = models.URLField(max_length=500, blank=True)
    contact_social_twitter = models.URLField(max_length=500, blank=True)
    contact_social_other = models.URLField(max_length=500, blank=True)

    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    project_type = models.CharField(max_length=128, blank=True, choices=TYPES)

    # Evaluation

    eval_version = models.IntegerField(default=1)
    phases = models.ManyToManyField(
        "ProjectPhase", through="ProjectAtPhase", blank=True
    )

    # UNESCO Knowledge Area
    knowledge_area = models.ForeignKey(
        "KnowledgeArea", blank=True, null=True, on_delete=models.SET_NULL
    )

    # TODO: RequestForResearch
    # request = models.ForeignKey("RequestForReseach", null=True, blank=True, on_delete=models.SET_NULL)
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
        return self.owner == user or self.managers.filter(pk=user.pk).exists()

    def is_participant(self, user):
        return (
            self.participants.filter(participation__user=user).exists()
            or self.managers.filter(pk=user.pk).exists()
        )

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
        if "project" not in data:
            return user.is_superuser

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
        if "project" not in data:
            return user.is_superuser

        # Special guard against adding "invited" users
        user = User.objects.get(pk=data["user"])
        if user.eval_token != '':
            return False
        
        # Check project write access
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

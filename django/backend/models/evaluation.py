from django.db import models
from django.dispatch import receiver
from django.conf import settings

from backend.models import TrackableModel, Participation, Project

# -----------------------
# Evaluation AXII
# -----------------------
AXIS_SCIENCE = "SCIENCE"
AXIS_COLLECTIVE = "COLLECTIVE"
AXIS_INDIVIDUAL = "INDIVIDUAL"

AXIS_CHOICES = [
    (AXIS_SCIENCE, "Science"),
    (AXIS_COLLECTIVE, "Collective"),
    (AXIS_INDIVIDUAL, "Individual"),
]

# -----------------------
# Evaluation Principles
# -----------------------
PRINCIPLE_KNOWLEDGE = "KNOWLEDGE"
PRINCIPLE_CITIZEN = "CITIZEN"
PRINCIPLE_PARTICIPATION = "PARTICIPATION"
PRINCIPLE_TRANSFORM = "TRANSFORM"
PRINCIPLE_INTEGRITY = "INTEGRITY"

PRINCIPLE_CHOICES = [
    (PRINCIPLE_KNOWLEDGE, "Knowledge Democracy"),
    (PRINCIPLE_CITIZEN, "Citizen-led Research"),
    (PRINCIPLE_PARTICIPATION, "Participatory Dynamics"),
    (PRINCIPLE_TRANSFORM, "Transformative Change"),
    (PRINCIPLE_INTEGRITY, "Integrity"),
]

# -----------------------
# Evaluation Dimencions
# -----------------------
DIM_COLLECTIVE = "COLLECTIVE"
DIM_ALIGNEMENT = "ALIGNEMENT"
DIM_ENGAGEMENT = "ENGAGEMENT"
DIM_EXPECTATION = "EXPECTATION"
DIM_GENDER = "GENDER"
DIM_PARTICIPATION_IMPACT = "PARTICIPATION_IMPACT"
DIM_INCLUSIVITY = "INCLUSIVITY"
DIM_KNOWLEDGE = "KNOWLEDGE"
DIM_MOTIVATION = "MOTIVATION"
DIM_OPENNESS = "OPENNESS"
DIM_POLICY_IMPACT = "POLICY_IMPACT"
DIM_REFLEXIVITY = "REFLEXIVITY"
DIM_RESOURCES = "RESOURCES"
DIM_RESPONSIVENESS = "RESPONSIVENESS"
DIM_SATISFACTION = "SATISFACTION"
DIM_RELEVANCE = "RELEVANCE"
DIM_SELFIMPROVE = "SELFIMPROVE"
DIM_TRANSDISCIPLINAR = "TRANSDISCIPLINAR"
DIM_TRANSPARENCY = "TRANSPARENCY"

DIMENSION_CHOICES = [
    (DIM_COLLECTIVE, "Collective capacity"),
    (DIM_ALIGNEMENT, "Community alignment"),
    (DIM_ENGAGEMENT, "Degree of engagement"),
    (DIM_EXPECTATION, "Expectation alignment"),
    (DIM_GENDER, "Gender perspective"),
    (DIM_PARTICIPATION_IMPACT, "Impact of the participatory dynamics"),
    (DIM_INCLUSIVITY, "Inclusivity"),
    (DIM_KNOWLEDGE, "Knowledge and skills"),
    (DIM_MOTIVATION, "Motivation"),
    (DIM_OPENNESS, "Openness"),
    (DIM_POLICY_IMPACT, "Policy impact"),
    (DIM_REFLEXIVITY, "Reflexivity"),
    (DIM_RESOURCES, "Resource availability"),
    (DIM_RESPONSIVENESS, "Responsiveness to community alignment"),
    (DIM_SATISFACTION, "Satisfaction with the participatory dynamics"),
    (DIM_RELEVANCE, "Scientific relevance"),
    (DIM_SELFIMPROVE, "Self-improvement"),
    (DIM_TRANSDISCIPLINAR, "Knowledge Integration"),  # Name changed for v2
    (DIM_TRANSPARENCY, "Transparency"),
]

# -----------------------
# Answer Types
# -----------------------
ANSWER_MULTIPLE = "MULTIPLE"
ANSWER_DEGREE = "DEGREE"
ANSWER_TEXT = "TEXT"
ANSWER_CHOICES = [
    (ANSWER_MULTIPLE, "Multiple Choice"),
    (ANSWER_DEGREE, "Degree"),
    (ANSWER_TEXT, "Text"),
]


class Question(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    version = models.IntegerField(default=1)

    axis = models.CharField(choices=AXIS_CHOICES, max_length=32)
    principle = models.CharField(choices=PRINCIPLE_CHOICES, max_length=32)
    dimension = models.CharField(choices=DIMENSION_CHOICES, max_length=32)
    role = models.ForeignKey("ParticipationRole", on_delete=models.SET_NULL, null=True)
    phase = models.ForeignKey("ProjectPhase", on_delete=models.SET_NULL, null=True)

    i18n = models.CharField(max_length=256, blank=True)
    # name = models.CharField(max_length=1024)

    answers = models.ManyToManyField("Answer", blank=True)
    answer_type = models.CharField(choices=ANSWER_CHOICES, max_length=32)
    answer_range = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return "Question [%s] %s" % (self.answer_type, self.i18n)

    class Meta:
        ordering = ["answer_type", "id"]


class Evaluation(TrackableModel):
    resend_email = models.BooleanField(default=False)
    participation = models.ForeignKey(
        "Participation", on_delete=models.CASCADE, null=True
    )
    phase = models.ForeignKey("ProjectAtPhase", on_delete=models.CASCADE, null=True)

    @property
    def is_complete(self):
        return self.response_set.count() > 0

    @property
    def project(self):
        if self.phase:
            return self.phase.project
        return None

    @property
    def project_phase(self):
        if self.phase:
            return self.phase.project_phase
        return None

    @property
    def questions(self):
        if self.project is None:
            return None

        # Filter questions by project's evaluation version as well as  role and phase
        all_questions = Question.objects
        version_questions = all_questions.filter(version=self.project.eval_version)
        phase_questions = version_questions.filter(phase=self.phase.project_phase)
        role_questions = phase_questions.filter(role=self.participation.role)

        return role_questions.all()

    @classmethod
    def can_create(cls, user, data):
        if "participation" not in data:
            return user.is_superuser

        participation = Participation.objects.get(pk=data["participation"])
        return participation.project.can_write(user)

    def can_read(self, user):
        return self.project.can_write(user) or self.participation.user == user

    def can_write(self, user):
        return self.project.can_write(user) or self.participation.user == user

    def __str__(self):
        return "Evaluation for %s (%s) by %s" % (
            self.project,
            self.phase.project_phase,
            self.participation.user,
        )

    class Meta:
        unique_together = ("participation", "phase")


@receiver(models.signals.post_save, sender=Evaluation)
def email_new_evaluation(
    sender, instance, raw, created, using, update_fields, **kwargs
):
    # TODO: Abort on shell scripts and such

    if isinstance(instance, Evaluation):
        # Don't send evaluation emails for Invited users
        user_eval_token = instance.participation.user.eval_token
        if user_eval_token != None and len(user_eval_token) > 0:
            print("No email for invited users")
            return

        # Send or resend email
        if created or instance.resend_email:
            instance.resend_email = False
            instance.save()

            from backend import email

            email.email_new_evaluation(instance)
            print("Sent email for new evaluation")


class Answer(models.Model):
    key = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=1024)

    def __str__(self):
        return "%d: %s" % (self.key, self.name[:50])

    class Meta:
        ordering = ["key"]


class Response(TrackableModel):
    evaluation = models.ForeignKey("Evaluation", on_delete=models.CASCADE, null=True)
    question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True)

    answer_multiple = models.ManyToManyField("Answer", blank=True)
    answer_choice = models.ForeignKey(
        "Answer",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="single_answers",
        related_query_name="single_answer",
    )
    answer_text = models.CharField(max_length=4096, blank=True)
    answer_degree = models.PositiveSmallIntegerField(blank=True, null=True)

    @property
    def project(self):
        if self.evaluation:
            return self.evaluation.project
        return None

    @property
    def project_pk(self):
        if self.evaluation:
            return self.evaluation.project.pk
        return None

    @property
    def answer_type(self):
        return self.question.answer_type

    class Meta:
        # Only one response per question per evaluation per person
        unique_together = ("evaluation", "question")

    def __str__(self):
        return f"{self.question.id} by {self.evaluation.participation.user}"

    @classmethod
    def can_create(cls, user, data):
        if "evaluation" not in data:
            return user.is_superuser

        evaluation = Evaluation.objects.get(pk=data["evaluation"])
        return (
            evaluation.project.can_write(user) or evaluation.participation.user == user
        )

    def can_read(self, user):
        return self.evaluation.participation.user == user or self.project.can_write(
            user
        )

    def can_write(self, user):
        return self.evaluation.participation.user == user or self.project.can_write(
            user
        )


@receiver(models.signals.post_save, sender=Response)
def invalidate_cache(sender, instance, raw, created, using, update_fields, **kwargs):
    """This receiver listes for any updated questionaire responses, and performs a
    cache invalidation of the entire CSV endpoint for evaluations."""

    if settings.CACHE_REDIS and isinstance(instance, Response):
        from django.core.cache import cache

        try:
            # Destroy all cached generated CSVs
            cache.delete_pattern("/v1/csv/eval/*")

            # Destroy response cache for this project
            project_id = instance.evaluation.phase.project.id
            cache.delete_pattern("/v1/csv/_responses/%d/*" % project_id)
        except Exception:
            pass

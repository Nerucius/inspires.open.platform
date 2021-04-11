from django.db import models
from django.dispatch import receiver

from backend.models import TrackableModel, User


class Structure(TrackableModel):

    TYPE_ACADEMIC_RESEARCH = "ACADEMIC_RESEARCH"
    TYPE_CIVIL_SOCIETY_ORG = "CIVIL_SOCIETY_ORG"
    TYPE_NGO_NON_PROFIT = "NGO_NON_PROFIT"
    TYPE_COMPANY = "COMPANY"
    TYPE_GOVERNMENT_ORG = "GOVERNMENT_ORG"
    TYPE_OTHER = "OTHER"

    TYPES = [
        (TYPE_ACADEMIC_RESEARCH, "Academic and/or Research"),
        (TYPE_CIVIL_SOCIETY_ORG, "Civil Society Association"),
        (TYPE_NGO_NON_PROFIT, "NGO and Non-Profit"),
        (TYPE_COMPANY, "Company or For-Profit"),
        (TYPE_GOVERNMENT_ORG, "Governmental Entity"),
        (TYPE_OTHER, "Other"),
    ]

    managers = models.ManyToManyField(
        User,
        blank=True,
        related_name="managed_structures",
        related_query_name="managed_structure",
    )

    name = models.CharField(max_length=254, unique=True)
    summary = models.TextField()
    year_founded = models.PositiveIntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=512, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    knowledge_areas = models.ManyToManyField("KnowledgeArea", blank=True)
    structure_type = models.CharField(max_length=254, blank=True, choices=TYPES)

    # TODO: this will have to be like the form for "participants"
    # funding = models.ManyToManyField("Funding")

    networks = models.ManyToManyField(
        "Network", blank=True, related_name="projects", related_query_name="project"
    )

    contact_email = models.EmailField(blank=True)
    contact_postal_address = models.TextField(blank=True)
    contact_website = models.URLField(max_length=500, blank=True)
    contact_social_facebook = models.URLField(max_length=500, blank=True)
    contact_social_twitter = models.URLField(max_length=500, blank=True)
    contact_social_other = models.URLField(max_length=500, blank=True)

    def can_write(self, user):
        return self.owner == user or self.managers.filter(pk=user.pk).exists()

    def __str__(self):
        return self.name

    @property
    def is_valid(self) -> bool:
        if hasattr(self, "validation"):
            return self.validation.is_approved
        return False


class StructureValidation(TrackableModel):
    is_approved = models.BooleanField(default=True)
    structure = models.OneToOneField(
        Structure, on_delete=models.CASCADE, related_name="validation", null=True
    )

    def __str__(self):
        if hasattr(self, "structure"):
            return "%s by %s" % (self.structure, self.created_by.username)
        return "by %s" % (self.created_by.username)


class Network(models.Model):

    name = models.CharField(max_length=254)
    summary = models.TextField()

    def __str__(self):
        return self.name


# Structure Data Triggers


@receiver(models.signals.post_save, sender=Structure)
def email_new_structure(sender, instance, raw, created, **kwargs):
    if not created:
        return

    from backend import email

    email.email_new_structure(instance)
    print("Sent email for new structure")


@receiver(models.signals.post_save, sender=StructureValidation)
def email_validated_structure(sender, instance, raw, created, **kwargs):
    if not instance.is_approved:
        return

    from backend import email

    email.email_structure_validated(instance)
    print("Sent email for validated structure")

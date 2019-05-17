from django.db import models
from django.dispatch import receiver

from backend.models import TrackableModel, User


class Structure(TrackableModel):

    managers = models.ManyToManyField(
        User,
        blank=True,
        related_name="managed_structures",
        related_query_name="managed_structure",
    )

    # validation = models.OneToOneField(
    #     "StructureValidation",
    #     related_name="structure",
    #     related_query_name="structure",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )

    name = models.CharField(max_length=254, unique=True)
    summary = models.TextField()
    year_founded = models.PositiveIntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=16, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    knowledge_areas = models.ManyToManyField("KnowledgeArea", blank=True)

    # TODO: Define if should be choice fields or foreign keys
    # structure_type = models.CharField(max_length=254)
    # structure_research_type = models.CharField(max_length=254)

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


@receiver(models.signals.post_save)
def email_new_structure(sender, instance, raw, created, using, update_fields, **kwargs):
    # TODO: Abort on shell scripts and such

    if created and isinstance(instance, Structure):
        from backend import email

        email.email_new_structure(instance)
        print("Sent email for new structure")


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

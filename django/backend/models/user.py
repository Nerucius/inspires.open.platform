from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from django.db import models

from backend.models import TrackableModel

from hashlib import md5


class User(TrackableModel, AbstractUser):
    """ Custom Application User. Is both a valid auth user and a trackable model. """

    GENDER_MALE = "MALE"
    GENDER_FEMALE = "FEMALE"
    GENDER_OTHER = "OTHER"

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]

    EDUCATION_PRIMARY = "PRIMARY"
    EDUCATION_SECONDARY = "SECONDARY"
    EDUCATION_TERTIARY = "TERTIARY"
    EDUCATION_DEGREE = "DEGREE"
    EDUCATION_MASTER = "MASTER"
    EDUCATION_DOCTORAL = "DOCTORAL"

    EDUCATION_LEVELS = [
        (EDUCATION_PRIMARY, "Primary"),
        (EDUCATION_SECONDARY, "Secondary"),
        (EDUCATION_TERTIARY, "Teriary (Labor market)"),
        (EDUCATION_DEGREE, "Bachelors or Degree"),
        (EDUCATION_MASTER, "Masters"),
        (EDUCATION_DOCTORAL, "Doctoral"),
    ]

    # Override email
    email = models.EmailField(_("email address"), blank=True, unique=True)

    email_verification = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=128, blank=True, null=True)

    education_level = models.CharField(
        max_length=128, blank=True, choices=EDUCATION_LEVELS
    )

    institution = models.CharField(max_length=256, blank=True)
    gender = models.CharField(max_length=256, blank=True, choices=GENDER_CHOICES)

    @property
    def is_administrator(self):
        return self.groups.filter(name="Administration").exists()

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def avatar_url(self):
        email = self.email.encode("ascii")
        default = "identicon"
        return "https://www.gravatar.com/avatar/%s.jpg?s=128&d=%s&r=g" % (
            md5(email).hexdigest(),
            default,
        )

    def can_create(self, user, data):
        return False

    def can_read(self, user):
        # return self.pk == user.pk
        # Since detailed user info includes project list and other details, we have to
        return True

    def can_write(self, user):
        """ Only the own user can modify the user info """
        return self.pk == user.pk

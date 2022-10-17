from datetime import time
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.utils import timezone

from backend.models import TrackableModel

from hashlib import md5
import urllib


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
        (EDUCATION_TERTIARY, "Tertiary (Labor market)"),
        (EDUCATION_DEGREE, "Bachelors or Degree"),
        (EDUCATION_MASTER, "Masters"),
        (EDUCATION_DOCTORAL, "Doctoral"),
    ]

    # Override email
    email = models.EmailField(_("email address"), blank=True, unique=True)
    email_verification = models.BooleanField(default=False)

    reset_password_token = models.CharField(max_length=128, blank=True, null=True)
    # Login token to log-in via URL
    eval_token = models.CharField(max_length=128, blank=True, null=True)

    hide_realname = models.BooleanField(default=False)

    # Profile
    # avatar_image_url = models.URLField(blank=True)
    education_level = models.CharField(
        max_length=128, blank=True, choices=EDUCATION_LEVELS
    )
    institution = models.CharField(max_length=256, blank=True)
    gender = models.CharField(max_length=256, blank=True, choices=GENDER_CHOICES)

    @property
    def is_administrator(self):
        return self.groups.filter(name="Administration").exists()

    @property
    def is_editor(self):
        return self.is_staff and self.groups.filter(name="Editors").exists()

    @property
    def first_name_anon(self):
        return self.first_name if not self.hide_realname else "Anonymous"

    @property
    def last_name_anon(self):
        pk_ascci = str(self.pk).encode("ascii")
        return (
            self.last_name
            if not self.hide_realname
            else md5(pk_ascci).hexdigest()[:6].upper()
        )

    @property
    def full_name(self):
        return "%s %s" % (self.first_name_anon, self.last_name_anon)

    @property
    def avatar_url(self):
        email = self.email.lower.encode("ascii")
        default = "identicon"

        gravatar_url = "https://www.gravatar.com/avatar/" + md5(email).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':128})

        return gravatar_url

    @property
    def evaluations(self):
        evaluations = []
        for part in self.participation_set.all():
            for eval in part.evaluation_set.all():
                evaluations += [eval]
        return evaluations

    def can_create(self, user, data):
        # Dedicated endpoint for this
        return False

    def can_read(self, user):
        # return self.pk == user.pk
        # Since detailed user info includes project list and other details, we have to
        return True

    def can_write(self, user):
        """ Only the own user can modify the user info """
        return self.pk == user.pk

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

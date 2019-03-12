from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation

from hashlib import md5

from backend.models import TrackableModel


class User(TrackableModel, AbstractUser):
    """ Custom Application User. Is both a valid auth user and a trackable model. """

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

    def can_read(self, user):
        """ Only the own user can view the detailed user info """
        return self.pk == user.pk

    def can_write(self, user):
        """ Only the own user can modify the user info """
        return self.pk == user.pk

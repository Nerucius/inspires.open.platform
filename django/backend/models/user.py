from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation

from hashlib import md5

from backend.models import TrackableModel


class User(TrackableModel, AbstractUser):
    """ Custom Application User. Is both a valid auth user and a trackable model. """

    @property
    def avatar_url(self):
        email = self.email.encode("ascii")
        return "https://www.gravatar.com/avatar/%s.jpg?s=128&d=mp&r=g" % (
            md5(email).hexdigest()
        )

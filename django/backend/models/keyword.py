from django.db import models


class Keyword(models.Model):
    """ Keywords are a way to tag projects that are related to the same
        general topic or area of research. They are fully translatable. """

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

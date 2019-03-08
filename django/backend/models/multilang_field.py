from django.db import models
from backend.models import TrackableModel


class MultilangField(TrackableModel):
    def text(self, lang="en"):
        match = self.entries.filter(lang=lang).all()
        if match:
            return match.text
        match = self.entries.first()
        if match:
            return match.text
        return "missing translation"

    def __str__(self):
        return "MLT: %s" % (self.text()[:20])


class MultilangFieldEntry(TrackableModel):

    field = models.ForeignKey(
        MultilangField,
        related_name="entries",
        related_query_name="entry",
        on_delete=models.CASCADE,
    )
    lang = models.CharField(max_length=16)
    text = models.TextField()

    def __str__(self):
        return "MLE: %s : %s" % (self.lang, self.text[:10])

    class Meta:
        verbose_name_plural = "Multilanguage entries"

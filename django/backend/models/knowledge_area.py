from django.db import models


class KnowledgeArea(models.Model):
    parent = models.ForeignKey(
        "KnowledgeArea", blank=True, null=True, on_delete=models.CASCADE
    )

    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return "[%s] %s" % (self.code, self.name)

    class Meta:
        ordering = ["code"]

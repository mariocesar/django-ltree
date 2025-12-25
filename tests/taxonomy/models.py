from django.db import models

from django_ltree.models import TreeModel


class Taxonomy(TreeModel):
    label_size = 2

    name = models.TextField()

    def __str__(self):
        return f"{self.name}"
        # return "{}: {}".format(self.path, self.name)

    def __repr__(self):
        return self.name

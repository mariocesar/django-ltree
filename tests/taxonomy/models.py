from django_ltree.managers import TreeManager
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


class TaxonomyName(TreeModel):
    name = models.TextField()

    t_objects = TreeManager(path_field="name")


class LegacyTaxonomy(TreeModel):
    """Opts out of label padding to keep pre-0.8 unpadded paths."""

    name = models.TextField()

    t_objects = TreeManager(label_width=None)

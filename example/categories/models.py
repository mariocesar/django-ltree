from django.db import models

from django_ltree.fields import PathField
from django_ltree.functions import NLevel


class Category(models.Model):
    name = models.CharField(max_length=140)
    path = PathField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.path

    def subcategories(self):
        return Category.objects.filter(
            path__descendant=self.path, path__nlevel=NLevel(self.path) + 1
        )

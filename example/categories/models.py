from django.db import models
from django_ltree.fields import PathField


class Category(models.Model):
    name = models.CharField(max_length=140)
    path = PathField(unique=True)

    def __str__(self):
        return self.path


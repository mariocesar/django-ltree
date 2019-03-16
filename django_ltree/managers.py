from django.db import models
from django.db.models.manager import BaseManager


class TreeQuerySet(models.QuerySet):
    def roots(self):
        return self.filter(path__depth=1)

    def childrens(self, *, path):
        return self.filter(path__descendants=path, path__depth=len(path) + 1)


class TreeManager(BaseManager.from_queryset(TreeQuerySet)):
    def get_queryset(self):
        return super().get_queryset().order_by("path")

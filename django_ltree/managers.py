from django.db import models

from django_ltree.fields import PathValue


class TreeQuerySet(models.QuerySet):
    def roots(self):
        return self.filter(path__depth=1)

    def children(self, path):
        return self.filter(path__descendants=path, path__depth=len(path) + 1)


class TreeManager(models.Manager):
    def get_queryset(self):
        return TreeQuerySet(model=self.model, using=self._db).order_by("path")

    def roots(self):
        return self.filter().roots()

    def children(self, path):
        return self.filter().children(path)

    def create_child(self, parent=None, **kwargs):
        prefix = parent.path if parent else None
        kwargs.pop("path", None)
        obj = self.create(**kwargs)

        if prefix:
            path = PathValue([*prefix, obj.id])
        else:
            path = PathValue([obj.id])
        self.filter(id=obj.id).update(path=path)

        obj.path = path

        return obj

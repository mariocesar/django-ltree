from django.db import models
from django.db.models.manager import BaseManager

from django_ltree.paths import PathGenerator


class TreeQuerySet(models.QuerySet):

    def roots(self):
        return self.filter(path__depth=1)

    def children(self, path):
        return self.filter(path__descendants=path, path__depth=len(path) + 1)


class TreeManager(BaseManager.from_queryset(TreeQuerySet)):

    def get_queryset(self):
        return super(TreeManager, self).get_queryset().order_by("path")

    def create_child(self, parent=None, **kwargs):
        paths_in_use = parent.children() if parent else self.roots()
        prefix = parent.path if parent else None
        path_generator = PathGenerator(prefix,
                                       skip=paths_in_use.values_list('path', flat=True),
                                       label_size=getattr(self.model, 'label_size'))
        kwargs['path'] = path_generator.next()
        return self.create(**kwargs)

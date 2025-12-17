from django.db import models
from django.db.models.functions import Concat


from .fields import PathField, PathValue

from .functions import NLevel, Subpath
from .managers import TreeManager


class TreeModel(models.Model):
    path = PathField(unique=True, null=True, blank=True)
    objects = TreeManager()

    class Meta:
        abstract = True
        ordering = ("path",)

    def label(self):
        return self.path[-1]

    def get_ancestors_paths(self):  # type: () -> List[List[str]]
        return [PathValue(self.path[:n]) for n, p in enumerate(self.path) if n > 0]

    def ancestors(self):
        return type(self)._default_manager.filter(path__ancestors=self.path)

    def descendants(self):
        return type(self)._default_manager.filter(path__descendants=self.path)

    def parent(self):
        if len(self.path) > 1:
            return self.ancestors().exclude(id=self.id).last()

    def children(self):
        return self.descendants().filter(path__depth=len(self.path) + 1)

    def siblings(self):
        parent = self.path[:-1]
        return (
            type(self)
            ._default_manager.filter(path__descendants=".".join(parent))
            .filter(path__depth=len(self.path))
            .exclude(path=self.path)
        )

    def add_child(self, path, **kwargs):  # type:(str) -> Any
        assert "path" not in kwargs
        kwargs["path"] = self.path[:]
        kwargs["path"].append(path)
        return type(self)._default_manager.create(**kwargs)

    def change_parent(self, new_parent):
        data = Concat(
            models.Value(new_parent.path, output_field=PathField()),
            Subpath(
                models.F("path"),
                NLevel(models.Value(str(self.path))) - 1,
            ),
        )
        type(self).objects.filter(path__descendants=self.path).update(path=data)

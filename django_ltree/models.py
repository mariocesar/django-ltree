from typing import Self

from django.contrib.postgres.indexes import BTreeIndex, GistIndex
from django.db import models
from django.db.models.functions import Concat


from .fields import PathField, PathValue

from .functions import NLevel, Subpath
from .managers import TreeManager


class TreeModel(models.Model):
    path: PathValue = PathField(unique=True, null=True, blank=True)  # pyright: ignore[reportAssignmentType]

    t_objects: TreeManager = TreeManager()

    class Meta:
        abstract = True
        ordering = ("path",)
        indexes = [BTreeIndex(fields=["path"]), GistIndex(fields=["path"])]

    def label(self) -> str:
        return self.path[-1]

    def get_ancestors_paths(self) -> list[PathValue]:
        return [PathValue(self.path[:n]) for n, _ in enumerate(self.path) if n > 0]

    def ancestors(self) -> models.QuerySet[Self]:
        return type(self).t_objects.filter(path__ancestors=self.path)

    def descendants(self) -> models.QuerySet[Self]:
        return type(self).t_objects.filter(path__descendants=self.path)

    def parent(self) -> Self | None:
        if len(self.path) > 1:
            return self.ancestors().exclude(id=self.id).last()  # pyright: ignore[reportReturnType, reportAttributeAccessIssue]

    def get_root(self) -> Self:
        func = Subpath(models.Value(str(self.path)), 0, 1)
        return type(self).t_objects.get(path=func)

    def children(self) -> models.QuerySet[Self]:
        return type(self).t_objects.filter(path__match=f"{self.path}.*{{1}}")

    def siblings(self) -> models.QuerySet[Self]:
        parent = self.path[:-1]
        return type(self).t_objects.filter(path__match=f"{parent}.*{{1}}").exclude(path=self.path)

    def add_child(self, **kwargs) -> Self:
        return type(self).t_objects.create_child(parent=self, **kwargs)

    def change_parent(self, new_parent: Self | PathValue) -> int:
        """
        move an item and all it's descendants under another item
        """
        new_p = new_parent.path if isinstance(new_parent, type(self)) else new_parent
        data = Concat(
            models.Value(new_p, output_field=PathField()),
            Subpath(
                models.F("path"),
                NLevel(models.Value(str(self.path))) - 1,
            ),
        )
        return type(self).t_objects.filter(path__descendants=self.path).update(path=data)

    def make_root(self) -> int:
        """replant a branch
        make this item a root element (no parents)
        all the descendants are moved as well
        """
        data = Subpath(
            models.F("path"),
            NLevel(models.Value(str(self.path))) - 1,
        )

        return type(self).t_objects.filter(path__descendants=self.path).update(path=data)

    def delete(self, cascade=False, **kwargs) -> tuple[int, dict[str, int]]:
        children = self.children()

        # keeping the descendants
        if not cascade:
            parent: PathValue = self.path[:-1]
            for c in children:
                # if there is a parent, move the children under that parent
                if parent:
                    c.change_parent(new_parent=parent)
                # if there is no parent, move the children to be root
                else:
                    c.make_root()

        # deleting all the descendants
        else:
            return self.delete_cascade(**kwargs)

        return super().delete(**kwargs)

    def delete_cascade(self, **kwargs) -> tuple[int, dict[str, int]]:
        """delete an item and all it's descendants"""
        return type(self).t_objects.filter(path__descendants=self.path).delete()

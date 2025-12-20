from django.db import models
from django.db.models.functions import Concat


from .fields import PathField, PathValue

from .functions import NLevel, Subpath
from .managers import TreeManager


class TreeModel(models.Model):
    path = PathField(unique=True, null=True, blank=True)
    t_objects = TreeManager()

    class Meta:
        abstract = True
        ordering = ("path",)

    def label(self):
        return self.path[-1]

    def get_ancestors_paths(self):  # type: () -> List[List[str]]
        return [PathValue(self.path[:n]) for n, p in enumerate(self.path) if n > 0]

    def ancestors(self):
        return type(self).t_objects.filter(path__ancestors=self.path)

    def descendants(self):
        return type(self).t_objects.filter(path__descendants=self.path)

    def parent(self):
        if len(self.path) > 1:
            return self.ancestors().exclude(id=self.id).last()

    def children(self):
        return type(self).t_objects.filter(path__match=f"{self.path}.*{{1}}")

    def siblings(self):
        parent = self.path[:-1]
        return type(self).t_objects.filter(path__match=f"{parent}.*{{1}}").exclude(path=self.path)

    def add_child(self, **kwargs):  # type:(str) -> Any
        return type(self).t_objects.create_child(parent=self, **kwargs)

    def change_parent(self, new_parent):
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
        type(self).t_objects.filter(path__descendants=self.path).update(path=data)

    def make_root(self):
        """replant a branch
        make this item a root element (no parents)
        all the descendants are moved as well
        """
        data = Subpath(
            models.F("path"),
            NLevel(models.Value(str(self.path))) - 1,
        )

        type(self).t_objects.filter(path__descendants=self.path).update(path=data)

    def delete(self, cascade=False, **kwargs):
        children: TreeModel = self.children()

        # keeping the descendants
        if not cascade:
            parent: TreeModel | None = self.parent()
            for c in children:
                # if there is a parent, move the children under that parent
                if parent:
                    c.change_parent(new_parent=parent)
                # if there is no parent, move the children to be root
                else:
                    c.make_root()

        # deleting all the descendants
        else:
            self.delete_cascade(**kwargs)

        return super().delete(**kwargs)

    def delete_cascade(self, **kwargs):
        """delete an item and all it's descendants"""
        return type(self).t_objects.filter(path__descendants=self.path).delete()

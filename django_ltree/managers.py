from typing import TYPE_CHECKING

from django.db import models

from django_ltree.fields import PathValue

if TYPE_CHECKING:
    from django_ltree.models import TreeModel


def resolve_path(node: "TreeModel | PathValue | str | list") -> PathValue:
    """
    Accept a model instance, PathValue, string, or list of labels and
    return the node's path as a PathValue.
    """
    if isinstance(node, models.Model):
        node = node.path  # ty:ignore[unresolved-attribute]
    path = node if isinstance(node, PathValue) else PathValue(node)
    if not path:
        raise ValueError("An empty path has no position in the tree")
    return path


class TreeQuerySet(models.QuerySet):
    def roots(self):
        return self.filter(path__depth=1)

    def children(self, node):
        return self.descendants_of(node, max_depth=1)

    def descendants_of(self, node, include_self=False, max_depth=None):
        path = resolve_path(node)
        min_depth = 0 if include_self else 1
        if max_depth is not None and max_depth < min_depth:
            raise ValueError("max_depth must be at least {}".format(min_depth))
        quantifier = "{{{},{}}}".format(min_depth, max_depth if max_depth is not None else "")
        return self.filter(path__match="{}.*{}".format(path, quantifier))

    def ancestors_of(self, node, include_self=False):
        path = resolve_path(node)
        qs = self.filter(path__ancestors=path)
        if not include_self:
            qs = qs.filter(path__depth__lt=len(path))
        return qs


class TreeManager(models.Manager):
    def __init__(self, path_field="id", *args, **kwargs):
        self.path_field = path_field
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return TreeQuerySet(model=self.model, using=self._db).order_by("path")

    def roots(self):
        return self.filter().roots()

    def children(self, node):
        return self.filter().children(node)

    def descendants_of(self, node, include_self=False, max_depth=None):
        return self.filter().descendants_of(node, include_self=include_self, max_depth=max_depth)

    def ancestors_of(self, node, include_self=False):
        return self.filter().ancestors_of(node, include_self=include_self)

    def create_child(self, parent: "TreeModel | PathValue | None" = None, **kwargs):
        """
        create an item
        `parent` can be an instance of the model or a PathValue object
        if `parent` is None, item will be a root item
        otherwise it'll be a child of that parent
        """
        kwargs.pop("path", None)
        if not parent:
            return self.create(**kwargs)

        prefix = parent.path if isinstance(parent, models.Model) else parent  # ty:ignore[unresolved-attribute]

        obj = self._create(**kwargs)

        path = PathValue([*prefix, getattr(obj, self.path_field)])
        self.filter(**{self.path_field: getattr(obj, self.path_field)}).update(path=path)

        obj.path = path

        return obj

    create_child.alters_data = True  # ty:ignore[unresolved-attribute]

    def create(self, **kwargs):
        """create an item with no parents (root)"""
        kwargs.pop("path", None)
        obj = self._create(**kwargs)

        path = PathValue([getattr(obj, self.path_field)])
        self.filter(**{self.path_field: getattr(obj, self.path_field)}).update(path=path)

        obj.path = path

        return obj

    create.alters_data = True  # ty:ignore[unresolved-attribute]

    def _create(self, **kwargs):
        """
        Create a new object with the given kwargs, saving it to the database
        and returning the created object.
        """
        reverse_one_to_one_fields = frozenset(kwargs).intersection(
            self.model._meta._reverse_one_to_one_field_names
        )
        if reverse_one_to_one_fields:
            raise ValueError(
                "The following fields do not exist in this model: %s"
                % ", ".join(reverse_one_to_one_fields)
            )

        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db)
        return obj

    _create.alters_data = True  # ty:ignore[unresolved-attribute]

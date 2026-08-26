from typing import TYPE_CHECKING

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from django_ltree.fields import PathValue

if TYPE_CHECKING:
    from django_ltree.models import TreeModel


LABEL_WIDTHS = {
    "SmallAutoField": 5,
    "SmallIntegerField": 5,
    "PositiveSmallIntegerField": 5,
    "AutoField": 10,
    "IntegerField": 10,
    "PositiveIntegerField": 10,
    "BigAutoField": 19,
    "BigIntegerField": 19,
    "PositiveBigIntegerField": 19,
}


def resolve_path(
    node: "TreeModel | PathValue | str | list", label_width: int | None = None
) -> PathValue:
    """
    Accept a model instance, PathValue, string, or list of labels and
    return the node's path as a PathValue.

    When `label_width` is given, numeric labels are zero-padded to that
    width to keep order consistent.
    """
    if isinstance(node, models.Model):
        node = node.path  # ty:ignore[unresolved-attribute]
    path = node if isinstance(node, PathValue) else PathValue(node)
    if not path:
        raise ValueError("An empty path has no position in the tree")
    if label_width:
        path = PathValue(
            [label.zfill(label_width) if label.isdigit() else label for label in path]
        )
    return path


class TreeQuerySet(models.QuerySet):
    label_width: int | None = None

    def _clone(self):
        clone = super()._clone()
        clone.label_width = self.label_width
        return clone

    def roots(self):
        return self.filter(path__depth=1)

    def children(self, node):
        return self.descendants_of(node, max_depth=1)

    def descendants_of(self, node, include_self=False, max_depth=None):
        path = resolve_path(node, self.label_width)
        min_depth = 0 if include_self else 1
        if max_depth is not None and max_depth < min_depth:
            raise ValueError("max_depth must be at least {}".format(min_depth))
        quantifier = "{{{},{}}}".format(min_depth, max_depth if max_depth is not None else "")
        return self.filter(path__match="{}.*{}".format(path, quantifier))

    def ancestors_of(self, node, include_self=False):
        path = resolve_path(node, self.label_width)
        qs = self.filter(path__ancestors=path)
        if not include_self:
            qs = qs.filter(path__depth__lt=len(path))
        return qs


class TreeManager(models.Manager):
    def __init__(self, path_field="id", label_width="auto", *args, **kwargs):
        self.path_field = path_field
        self.label_width = label_width
        super().__init__(*args, **kwargs)

    def resolve_label_width(self) -> int | None:
        """The effective label width for this manager."""
        if self.label_width != "auto":
            return self.label_width
        try:
            field = self.model._meta.get_field(self.path_field)
        except FieldDoesNotExist:
            return None
        return LABEL_WIDTHS.get(field.get_internal_type())

    def get_queryset(self):
        queryset = TreeQuerySet(model=self.model, using=self._db)
        queryset.label_width = self.resolve_label_width()
        return queryset.order_by("path")

    def format_label(self, value) -> str:
        """Build a path label from an item's `path_field` value."""
        label = str(value)
        label_width = self.resolve_label_width()
        if label_width and label.isdigit():
            if len(label) > label_width:
                raise ValueError(
                    "Label {!r} does not fit in label_width={}; labels wider than "
                    "the configured width would break sibling ordering".format(label, label_width)
                )
            return label.zfill(label_width)
        return label

    def roots(self):
        return self.filter().roots()

    def children(self, node):
        return self.filter().children(node)

    def descendants_of(self, node, include_self=False, max_depth=None):
        return self.filter().descendants_of(node, include_self=include_self, max_depth=max_depth)

    def ancestors_of(self, node, include_self=False):
        return self.filter().ancestors_of(node, include_self=include_self)

    def create_child(self, parent: "TreeModel | PathValue | str | list | None" = None, **kwargs):
        """
        create an item `parent` can be an instance of the model, a PathValue, a string
        like "1.2.3", or a list of labels
        """
        kwargs.pop("path", None)
        if not parent:
            return self.create(**kwargs)

        prefix = resolve_path(parent, self.resolve_label_width())

        obj = self._create(**kwargs)

        path = PathValue([*prefix, self.format_label(getattr(obj, self.path_field))])
        self.filter(**{self.path_field: getattr(obj, self.path_field)}).update(path=path)

        obj.path = path

        return obj

    create_child.alters_data = True  # ty:ignore[unresolved-attribute]

    def create(self, **kwargs):
        """create an item with no parents (root)"""
        kwargs.pop("path", None)
        obj = self._create(**kwargs)

        path = PathValue([self.format_label(getattr(obj, self.path_field))])
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

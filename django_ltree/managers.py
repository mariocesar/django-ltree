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

    _create.alters_data = True

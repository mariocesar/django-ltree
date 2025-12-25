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

    def create_child(self, parent: models.Model | PathValue | None = None, **kwargs):
        """
        create an item
        `parent` can be an instance of the model or a PathValue object
        if `parent` is None, item will be a root item
        otherwise it'll be a child of that parent
        """
        kwargs.pop("path", None)
        if not parent:
            return self.create(**kwargs)

        prefix = parent.path if isinstance(parent, models.Model) else parent

        obj = self._create(**kwargs)

        path = PathValue([*prefix, obj.id])
        self.filter(id=obj.id).update(path=path)

        obj.path = path

        return obj

    create_child.alters_data = True

    def create(self, **kwargs):
        """create an item with no parents (root)"""
        kwargs.pop("path", None)
        obj = self._create(**kwargs)

        path = PathValue([obj.id])
        self.filter(id=obj.id).update(path=path)

        obj.path = path

        return obj

    create.alters_data = True

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

# django-ltree

A Django implementation for PostgreSQL's ltree extension, providing efficient storage and querying of hierarchical tree-like data.

See PostgreSQL's [ltree](https://www.postgresql.org/docs/current/ltree.html) documentation to learn
more about it.

The main benefits of `ltree`:

- Efficient path queries (ancestors, descendants, pattern matching)
- Index-friendly hierarchical storage
- Powerful label path searching
- Native PostgreSQL performance for tree operations

[![Test](https://github.com/mariocesar/django-ltree/actions/workflows/test.yml/badge.svg)](https://github.com/mariocesar/django-ltree/actions/workflows/test.yml)
[![PyPI Version](https://img.shields.io/pypi/v/django-ltree.svg)](https://pypi.org/project/django-ltree/)

## Features

- Django model fields for ltree data types
- Query utilities for common tree operations
- Migration support for ltree extension installation
- Compatibility with Django's ORM and query syntax

## Requirements

- Django 5.2+
- Python 3.11+
- PostgreSQL 16+ (with ltree extension enabled)

## Installation

1. Install the package:

   ```bash
   pip install django-ltree
   ```

2. Add to your `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       ...
       "django_ltree",
       ...
   ]
   ```

3. Run migrations to install the ltree extension:

   ```bash
   python manage.py migrate django_ltree
   ```

## Usage

`django-ltree` provides a base model class called `TreeModel`.

`TreeModel` does these things out of the box:

- adds a field called `path` to your model (by default, path is created by items Id plus parent's path)
- adds `t_objects` which is the `TreeManager` you can use to work with tree data
- adds two indexes for `path` (one `BTreeIndex`, one `GistIndex`)
- orders items base on `path`

if you are overriding the `Meta` class of your model, you may want to inherit from TreeModel.Meta.

```py
  class Meta(TreeModel.Meta):
```

to keep the indexes and ordering.


## Quick Start

1. inherit from TreeModel:

   ```python
   from django_ltree.models import TreeModel

   class Category(TreeModel):
       name = models.CharField(max_length=50)
   ```

2. Create tree nodes:

   ```python
   # make an item without a parent (root)
   root = Category.t_objects.create(name="Root")
   # make a child item
   child = Category.t_objects.create_child(name="Child", parent=root)
   # you can also use `add_child` directly on root
   child2 = root.add_child(name="another child")
   ```

note that `path` is handled by `django-ltree`, you don't need to pass any value for it

3. Query ancestors and descendants:

   ```python
   # Get all ancestors
   child.ancestors()

   # Get all descendants
   child.descendants()
   ```


### Alternate paths

paths are made using the objects `id` and (if exists) it's parent's path.

if you need to use a different field for path generation, configure it like this:

```py
  class Role(TreeModel):
      name = CharField()

      t_objects = TreeManager(path_field="name")
```

now paths are created using the `name` field

```py
  su = Role.t_objects.create(name="SuperUser")
  print(su.path)  # SuperUser
  admin = su.add_child(name="Admin")
  print(admin.path)  # SuperUser.Admin
```

when using an alternative field for path generation, it is recommended to use a
field that ensures uniqueness to avoid confilicts.

if you are using a field that is not auto-generated (like name in the example
above), it is recommended to overwrite `TreeManager.create` and
`TreeManager.create_child` like this:

```py
class MyTreeManager(TreeManager):
    def create(self, **kwargs):
        """create an item with no parents (root)"""
        kwargs["path"] = PathValue([kwargs[self.path_field]])
        obj = self._create(**kwargs)

        return obj

    def create_child(self, parent: "TreeModel | PathValue | None" = None, **kwargs):
        if not parent:
            return self.create(**kwargs)

        prefix = parent.path if isinstance(parent, models.Model) else parent
        kwargs["path"] = PathValue([*prefix, kwargs[self.path_field]])

        obj = self._create(**kwargs)
        return obj
```

for slightly better performance and less overhead.

this does not work for auto-generated fields like `id`.

### TreeModel methods

`TreeModel` has the following methods:

1. `label(self)`: returns the last part of `path`

2. `ancestors(self)`: return all the ancestors of the current item, including the item itself
(use `t_objects.ancestors_of(item)` if you don't want the item included)

3. `descendants(self)`: return all the descendants of the current item, including the item itself
(use `t_objects.descendants_of(item)` if you don't want the item included)

4. `parent(self)`: return the immediate parent of the current item, or `None` if the item is a root

5. `get_root(self)`: return the root parent of this item

6. `children(self)`: return all the immediate children of the current item

7. `siblings(self)`: return all the siblings of the current item (items that share the same parent with this item), not including the item itself

8. `add_child(self, **kwargs)`: create a child for this item
kwargs are the arguments used to make the child (the model fields)

9. `get_ancestors_paths(self)`: return the paths of all the ancestors of the current item (not including the item's own path) as a list of `PathValue`

10. `change_parent(self, new_parent)`: change the parent of the current item (this moves the item and all it's descendants to be under another item)
new_parent is either a object of the same model, or the `path` value of an object
returns the number of rows updated

11. `make_root(self)`: move the current item to be a root item (moves the item and all it's descendants)
returns the number of rows updated

12. `delete(self, cascade=False, **kwargs)`: deletes the current item
if cascade is True, all the descendants are also deleted, otherwise the children will move under the deleted item's parent (or become root items if the deleted item was a root)

13. `delete_cascade(self, **kwargs)`: delete the current item and all it's descendants


### TreeManager methods

`TreeManager` has the following methods

1. `create_child(self, parent=None, **kwargs)`: creates an item
if `parent` is provided, it will become the parent item of the created item, otherwise creation will happen as root
`parent` can be a model instance or a `PathValue`
`kwargs` are the model fields used to create the item (any `path` passed in is ignored, it is always generated)

2. `create(self, **kwargs)`: create a root item
`kwargs` are the model fields used to create the item (any `path` passed in is ignored, it is always generated)

3. `roots(self)`: return all the root items from database

4. `children(self, node)`: return all the immediate children of `node`
`node` can be a model instance, a `PathValue`, a string like `"1.2.3"`, or a list of labels

5. `descendants_of(self, node, include_self=False, max_depth=None)`: return the descendants of `node`
by default the node itself is not included, pass `include_self=True` to include it
`max_depth` limits how many levels below the node to include this compiles to a
single indexed `lquery` match, e.g. `path ~ '1.2.*{1,3}'`

6. `ancestors_of(self, node, include_self=False)`: return the ancestors of `node`
by default the node itself is not included, pass `include_self=True` to include it

```python
# the whole subtree under a category, excluding the category itself
Category.t_objects.descendants_of(category)

# only two levels deep, e.g. for building a menu
Category.t_objects.descendants_of(category, max_depth=2)

# breadcrumbs: all ancestors from the root down, including the item
Category.t_objects.ancestors_of(category, include_self=True)
```

`roots`, `children`, `descendants_of`, and `ancestors_of` are also available on
querysets, so they can be chained with regular filters:

```python
Category.t_objects.filter(is_active=True).descendants_of(category, max_depth=2)
```

### lookups and functions

for a list of all available operations and functions for ltree check <https://www.postgresql.org/docs/current/ltree.html#LTREE-OPS-FUNCS>

#### provided lookups

1. `exact` (same as `=` in postgresql)
`TreeModel.t_objects.filter(path__exact=path)`

2. `ancestors` (same as `@>` in postgresql)
`TreeModel.t_objects.filter(path__ancestors=path)`

3. `descendants` (same as `<@` in postgresql)
`TreeModel.t_objects.filter(path__descendants=path)`

4. `match` (same as `~` in postgresql)
`TreeModel.t_objects.filter(path__match=f"{self.path}.*{{1}}")`

5. `contains` (same as `?` in postgresql)
takes a list (or tuple) of lquery patterns and matches items whose path matches any of them; passing a single string raises a `TypeError`
`TreeModel.t_objects.filter(path__contains=["1.*", "2.*"])`

6. `depth` (calls `NLEVEL` function from postgresql)
`TreeModel.t_objects.filter(path__depth=len(path) + 1)`
it is a transform, so it can be combined with other lookups, e.g. `path__depth__lt=3`

#### provided functions

1. `django_ltree.functions.NLevel`
same as NLEVEL function from postgresql

2. `django_ltree.functions.Subpath`
same as `SUBPATH` functions from postgresql

for concatenation (`||`) you can use `django.db.models.functions.Concat`


## Documentation

For complete documentation, see [TODO: Add Documentation Link].

## Links

- **Source Code**: <https://github.com/mariocesar/django-ltree>
- **Bug Reports**: <https://github.com/mariocesar/django-ltree/issues>
- **PyPI Package**: <https://pypi.org/project/django-ltree/>
- **PostgreSQL ltree Docs**: <https://www.postgresql.org/docs/current/ltree.html>

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/mariocesar/django-ltree/blob/main/CONTRIBUTING.md) for guidelines.

## License

[MIT License](https://github.com/mariocesar/django-ltree/blob/main/LICENSE)

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
- PostgreSQL 14+ (with ltree extension enabled)

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

* adds a field called `path` to your model (path is created by items Id plus all parent Ids)
* adds `t_objects` which is the `TreeManager` you can use to work with tree data
* adds two indexes for `path` (one `BTreeIndex`, one `GistIndex`)
* orders items base on `path`

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

### TreeModel methods
`TreeModel` has the following methods:

1. `label(self)`: returns the last part of `path`

2. `ancestors(self)`: return all the ancestors of the current item

3. `descendants(self)`: return all the descendants of the current item

4. `parent(self)`: return the immediate parent of the current item

5. `get_root(self)`: return the root parent of this item

6. `children(self)`: return all the immediate children of the current item

7. `siblings(self)`: return all the siblings of the current item (items that share the same parent with this item)

8. `add_child(self, **kwargs)`: create a child for this item
kwargs are the arguments used to make the child (the model fields)

9. `change_parent(self, new_parent)`: change the parent of the current item (this moves the item and all it's descendants to be under another item)
new_parent is either a object of the same model, or the `path` value of an object

10. `make_root(self)`: move the current item to be a root item (moves the item and all it's descendants)

11. `delete(self, cascade=False, **kwargs)`: deletes the current item
if cascade is True, all the descendants are also deleted, otherwise they will move to become the descendants of the first parent of the deleted item

12. `delete_cascade(self, **kwargs)`: delete the current item and all it's children


### TreeManager methods
`TreeManager` has the following methods
1. `create_child(self, parent=None, **kwargs)`: creates an item
if `parent` is provided, it will become the parent item of the created item, otherwise creation will happen as root
`kwargs` are the model fields used to create the item

2. `create(self, **kwargs)`: create a root item
`kwargs` are the model fields used to create the item

3. `roots(self)`: return all the root items from database

4. `children(self, path)`: return all the children of the specified `path`


### lookups and functions
for a list of all available operations and functions for ltree check https://www.postgresql.org/docs/current/ltree.html#LTREE-OPS-FUNCS

#### provided lookups:
1. `exact` (same as `=` in postgresql)
`TreeModel.t_objects.filter(path__exact=path)`

2. `ancestors` (same as `@>` in postgresql) 
`TreeModel.t_objects.filter(path__ancestors=path)`

3. `descendants` (same as `<@` in postgresql)
`TreeModel.t_objects.filter(path__descendants=path)`

4. `match` (same as `~` in postgresql)
`TreeModel.t_objects.filter(path__match=f"{self.path}.*{{1}}")`

5. `contains` (same as `?` in postgresql)
`TreeModel.t_objects.filter(path__contains="1.*")`

6. `depth` (calls `NLEVEL` function from postgresql)
`TreeModel.t_objects.filter(path__depth=len(path) + 1)`

#### provided functions
1. `django_ltree.functions.NLevel`
same as NLEVEL function from postgresql

2. `django_ltree.functions.Subpath`
same as `SUBPATH` functions from postgresql


for concatenation (`||`) you can use `django.db.models.functions.Concat`




## Known Issues

- Since PostgreSQL 16, the `-` character is also permitted. The tests in this repository expect version 16 or higher. If you're using PostgreSQL 15 or earlier, make sure to exclude `-` from labels.

## Documentation

For complete documentation, see [TODO: Add Documentation Link].

## Links

- **Source Code**: https://github.com/mariocesar/django-ltree
- **Bug Reports**: https://github.com/mariocesar/django-ltree/issues
- **PyPI Package**: https://pypi.org/project/django-ltree/
- **PostgreSQL ltree Docs**: https://www.postgresql.org/docs/current/ltree.html

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/mariocesar/django-ltree/blob/main/CONTRIBUTING.md) for guidelines.

## License

[MIT License](https://github.com/mariocesar/django-ltree/blob/main/LICENSE)

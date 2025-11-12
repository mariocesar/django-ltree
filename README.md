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

- Django 4.2+
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

4. Alternatively you can avoid install the application, and create the the extensions with a custom migration in an app in your project.

    ```python
    from django.db import migrations
    from django_ltree.operations import LtreeExtension

    class Migration(migrations.Migration):
        initial = True
        dependencies = []

        operations = [LtreeExtension()]
    ```

## Quick Start

1. Add a PathField to your model:
   ```python
   from django_ltree.fields import PathField

   class Category(models.Model):
       name = models.CharField(max_length=50)
       path = PathField()
   ```

2. Create tree nodes:
   ```python
   root = Category.objects.create(name="Root", path="root")
   child = Category.objects.create(name="Child", path=f"{root.path}.child")
   ```

3. Query ancestors and descendants:
   ```python
   # Get all ancestors
   Category.objects.filter(path__ancestor=child.path)

   # Get all descendants
   Category.objects.filter(path__descendant=root.path)
   ```

## Migration Dependency

Include django_ltree as a dependency in your app's migrations:

```python
class Migration(migrations.Migration):
    dependencies = [
        ("django_ltree", "__latest__"),
    ]
```

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

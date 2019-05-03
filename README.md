# django-ltree

An ltree extension implementation to support hierarchical tree-like data in django models

Postgresql has already a optimized and very useful tree implementation for data.
The extension is [ltree](https://www.postgresql.org/docs/9.6/static/ltree.html)

## Links

- Pypi https://pypi.org/project/django-ltree/
- Source code https://github.com/mariocesar/django-ltree
- Bugs https://github.com/mariocesar/django-ltree/issues
- Contribute https://github.com/mariocesar/django-ltree/pulls

- Documentation `TODO`

[![PyPI version](https://badge.fury.io/py/django-ltree.svg)](https://badge.fury.io/py/django-ltree)

## Install

    pip install django-ltree

Then add `django_ltree` to `INSTALLED_APPS` in your Django project settings.

And make sure to run `django_ltree` migrations before you added the `PathField`

    python manage.py migrations django_ltree

This will install the `ltree` extension

Requires:

- Django 2.0 or superior
- Python 3.6 or superior


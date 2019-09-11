import importlib

from django.apps import AppConfig


class DjangoLtreeConfig(AppConfig):
    name = "django_ltree"

    def ready(self):
        importlib.import_module("django_ltree.checks")
        importlib.import_module("django_ltree.lookups")
        importlib.import_module("django_ltree.functions")

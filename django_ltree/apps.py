import importlib

from django.apps import AppConfig


def register_pathfield():
    # Register field checks, lookups and functions
    importlib.import_module("django_ltree.checks")
    importlib.import_module("django_ltree.lookups")
    importlib.import_module("django_ltree.functions")


class DjangoLtreeConfig(AppConfig):
    name = "django_ltree"

    def ready(self):
        register_pathfield()

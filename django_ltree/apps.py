from django.apps import AppConfig


class DjangoLtreeConfig(AppConfig):
    name = 'django_ltree'

    def ready(self):
        from django_ltree import checks


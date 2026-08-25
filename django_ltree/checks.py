from django.core.checks import Error, Tags, register
from django.db import connections, router

MINIMUM_POSTGRES_VERSION = 16


@register(Tags.database)
def check_database_is_supported_postgres(app_configs, databases=None, **kwargs):
    errors = []

    for alias in databases or []:
        if not router.allow_migrate(alias, "django_ltree"):
            continue

        connection = connections[alias]

        if connection.vendor != "postgresql":
            errors.append(
                Error(
                    "django_ltree requires a PostgreSQL database; connection '{}' uses "
                    "the '{}' backend.".format(alias, connection.vendor),
                    hint=(
                        "Use 'django.db.backends.postgresql' or a compatible engine, or "
                        "add a database router that excludes 'django_ltree' from this "
                        "database."
                    ),
                    id="django_ltree.E002",
                )
            )
        elif connection.pg_version < MINIMUM_POSTGRES_VERSION * 10000:
            errors.append(
                Error(
                    "django_ltree requires PostgreSQL {} or newer; database connection "
                    "'{}' is PostgreSQL {}.".format(
                        MINIMUM_POSTGRES_VERSION, alias, connection.pg_version // 10000
                    ),
                    id="django_ltree.E001",
                )
            )

    return errors

from django.core.checks import Warning, register


@register
def check_database_backend_is_postgres(app_configs, **kwargs):
    from django.conf import settings

    errors = []
    valid_dbs = ["postgres", "postgis"]

    if "default" in settings.DATABASES and all(
        d not in settings.DATABASES["default"]["ENGINE"] for d in valid_dbs
    ):
        errors.append(
            Warning(
                (
                    "The 'django_ltree' package requires a PostgreSQL-compatible database engine "
                    "to enable the 'ltree' extension."
                ),
                hint=(
                    "Ensure your DATABASES setting uses 'django.db.backends.postgresql' or a "
                    "compatible engine. If using a custom backend for PostgreSQL, you may safely "
                    "ignore this warning."
                ),
                id="django_ltree.W001",
            )
        )

    return errors

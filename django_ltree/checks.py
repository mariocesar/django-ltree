from django.core.checks import Warning, register


@register
def check_database_backend_is_postgres(app_configs, **kwargs):
    from django.conf import settings
    errors = []
    valid_dbs=['postgres', 'postgis']
    if not any(d in settings.DATABASES['default']['ENGINE'] for d in valid_dbs):
        errors.append(Warning(
            'django_ltree needs postgres to support install the ltree extension.',
            hint='Use the postgres engine or ignore if you already use a custom engine for postgres'))

    return errors


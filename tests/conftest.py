try:
    import django
    from django.conf import settings
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements.txt")


def pytest_sessionstart(session):
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'ltree_test',
                'HOST': 'localhost',
                'USER': 'postgres'
            }
        },
        ROOT_URLCONF='tests.urls',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django_ltree',
            'taxonomy',
        ],
        SITE_ID=1,
    )
    django.setup()

import os

DEBUG = True
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "taxonomy_db",
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "postgres"),
        "PORT": os.environ.get("DJANGO_DATABASE_PORT", 5432),
    }
}
ROOT_URLCONF = "tests.conf.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_ltree",
    "tests.taxonomy",
    "django_harlequin",
]
SITE_ID = 1
SILENCED_SYSTEM_CHECKS = ["RemovedInDjango30Warning"]

from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations

from django_ltree.operations import LtreeExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [LtreeExtension(), BtreeGistExtension()]

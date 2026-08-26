import django.contrib.postgres.indexes
import django.db.models.manager
import django_ltree.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taxonomy", "0003_taxonomyname"),
    ]

    operations = [
        migrations.CreateModel(
            name="LegacyTaxonomy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "path",
                    django_ltree.fields.PathField(blank=True, null=True, unique=True),
                ),
                ("name", models.TextField()),
            ],
            options={
                "ordering": ("path",),
                "abstract": False,
                "indexes": [
                    django.contrib.postgres.indexes.BTreeIndex(
                        fields=["path"], name="taxonomy_le_path_1cc604_btree"
                    ),
                    django.contrib.postgres.indexes.GistIndex(
                        fields=["path"], name="taxonomy_le_path_9f27d3_gist"
                    ),
                ],
            },
            managers=[
                ("t_objects", django.db.models.manager.Manager()),
            ],
        ),
    ]

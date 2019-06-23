# Generated by Django 2.1.2 on 2018-10-06 15:12

from django.db import migrations, models
import django_ltree.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
            ('django_ltree', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('path', django_ltree.fields.PathField(unique=True)),
            ],
        ),
    ]

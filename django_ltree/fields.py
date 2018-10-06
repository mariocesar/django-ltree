from django.db.models.fields import TextField
from django.core.validators import RegexValidator
from django import forms
from django.forms.widgets import TextInput


path_label_validator = RegexValidator(
    r'^[A-Za-z0-9_.]+$',
    'A label is a sequence of alphanumeric characters and underscores separated by dots.',
    'invalid')


class PathFormField(forms.CharField):
    default_validators = [path_label_validator]


class PathField(TextField):
    default_validators = [path_label_validator]

    def db_type(self, connection):
        return 'ltree'

    def formfield(self, **kwargs):
        kwargs['form_class'] = PathFormField
        kwargs['widget'] = TextInput(attrs={'class': 'vTextField'})
        return super().formfield(**kwargs)


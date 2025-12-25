from django import forms

from .validators import path_label_validator


class PathFormField(forms.CharField):
    default_validators = [path_label_validator]

from django import forms
from django.core.validators import RegexValidator
from django.db.models.fields import TextField
from django.forms.widgets import TextInput
from six import string_types


class PathValue(list):
    def __init__(self, val):  # type: (Union[list, str]) -> None
        if isinstance(val, str):
            val = val.split(".")
        elif isinstance(val, list):
            val = val
        else:
            raise ValueError("Invalid value for path: {}".format(val))

        super(PathValue, self).__init__(val)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ".".join(self)


class PathValueProxy:
    def __init__(self, field_name):  # type: (str) -> None
        self.field_name = field_name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = instance.__dict__[self.field_name]

        if value is None:
            return value

        return PathValue(instance.__dict__[self.field_name])

    def __set__(self, instance, value):
        if instance is None:
            return self

        instance.__dict__[self.field_name] = value


path_label_validator = RegexValidator(
    r"^[A-Za-z0-9_.]+$",
    "A label is a sequence of alphanumeric characters and underscores separated by dots.",
    "invalid",
)


class PathFormField(forms.CharField):
    default_validators = [path_label_validator]


class PathField(TextField):
    default_validators = [path_label_validator]

    def db_type(self, connection):
        return "ltree"

    def formfield(self, **kwargs):
        kwargs["form_class"] = PathFormField
        kwargs["widget"] = TextInput(attrs={"class": "vTextField"})
        return super(PathField, self).formfield(**kwargs)

    def contribute_to_class(self, cls, name, private_only=False):
        super(PathField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, PathValueProxy(self.name))

    def from_db_value(self, value, expression, connection, *args):
        if value is None:
            return value
        return PathValue(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(PathValue(value))

    def to_python(self, value):
        if value is None:
            return value
        elif isinstance(value, PathValue):
            return value

        return PathValue(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        elif isinstance(value, PathValue):
            return str(value)
        elif isinstance(value, (list, string_types)):
            return str(PathValue(value))

        raise ValueError("Unknown value type {}".format(type(value)))

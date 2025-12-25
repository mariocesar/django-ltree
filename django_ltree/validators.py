from django.core.validators import RegexValidator


path_label_validator = RegexValidator(
    r"^(?P<root>[a-zA-Z0-9_-]+)(?:\.[a-zA-Z0-9_-]+)*$",
    "A label is a sequence of alphanumeric characters and underscores separated by dots or slashes.",  # noqa: E501
    "invalid",
)

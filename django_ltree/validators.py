from django.core.validators import RegexValidator


# Hyphens in labels require PostgreSQL 16+, the minimum version this package supports.
path_label_validator = RegexValidator(
    r"^(?P<root>[a-zA-Z0-9_-]+)(?:\.[a-zA-Z0-9_-]+)*$",
    "A path is a sequence of labels (letters, digits, underscores, and hyphens) separated by dots.",  # noqa: E501
    "invalid",
)

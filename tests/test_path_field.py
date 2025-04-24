import pytest
from django.core.exceptions import ValidationError
from taxonomy.models import Taxonomy

from django_ltree.fields import PathValue


@pytest.mark.parametrize(
    ["path", "valid"],
    [
        ("00_00a", True),
        ("00$00", False),
        ("00000a.00000b", True),
        ("00000a+00000b", False),
    ],
)
def test_path_field_validation(path, valid):
    """Validating that the path field is valid."""
    taxonomy = Taxonomy()
    taxonomy.name = "test"
    taxonomy.path = PathValue(path)
    if valid:
        taxonomy.full_clean()
    else:
        with pytest.raises(ValidationError) as excinfo:
            taxonomy.full_clean()

        assert excinfo.value.message_dict == {
            "path": [
                "A label is a sequence of alphanumeric characters and underscores separated by dots."
            ]
        }

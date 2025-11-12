import pytest
from django.core.exceptions import ValidationError
from taxonomy.models import Taxonomy

from django_ltree.fields import PathValue, path_label_validator


@pytest.mark.parametrize(
    ["path", "valid"],
    [
        ("abcABC-_ ", True),
        ("00_00a", True),
        ("00$00", False),
        ("00:00", False),
        ("00/00", True),  # slashes are allowed and converted to dots
        ("00000a+00000b", False),
        ("00000a.00000b.00000c", True),
        ("00000a..00000b", False),
        ("00000a.00000b.00000c.00000d", True),
        ("00000a.00000b.00000c.00000d.00000e.", False),
        # UUID like segments
        ("550e8400-e29b-41d4-a716-446655440000", True),
        ("550e8400-e29b-41d4-a716-446655440000.123e4567-e89b-12d3-a456-426614174000", True),
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

        assert excinfo.value.message_dict == {"path": [path_label_validator.message]}


@pytest.mark.parametrize(
    "input_path",
    [
        "root/child/grandchild",
        "root.child.grandchild",
        PathValue("root/child/grandchild"),
        PathValue("root.child.grandchild"),
    ],
)
def test_slash_in_path_field(input_path):
    """Test that slashes in path field are converted to dots."""
    taxonomy = Taxonomy()
    taxonomy.name = "test"
    taxonomy.path = input_path

    assert str(taxonomy.path) == "root.child.grandchild"


def test_mixing_slash_and_dot_in_path_field():
    """Test that mixing slashes and dots raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        PathValue("root/child.grandchild")

    assert str(excinfo.value) == "PathValue cannot mix slashes and dots in the same value"
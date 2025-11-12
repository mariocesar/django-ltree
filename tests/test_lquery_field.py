import pytest

from django_ltree.fields import LqueryField

pytestmark = pytest.mark.django_db


def test_lquery_field_db_type():
    """Test that LqueryField returns correct database type."""
    field = LqueryField()

    assert field.db_type(connection=None) == "lquery"
    assert field.editable is False

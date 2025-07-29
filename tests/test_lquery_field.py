from django.contrib.postgres.fields import ArrayField
from django.db.models import Value
from taxonomy.models import Taxonomy

from django_ltree.fields import LqueryField, PathField


def test_lquery_field_db_type():
    """Test that LqueryField returns correct database type."""
    field = LqueryField()
    assert field.db_type(connection=None) == "lquery"


def test_lquery_field_inherits_from_pathfield():
    """Test that LqueryField inherits PathField functionality."""
    field = LqueryField()
    assert isinstance(field, PathField)

    # Should inherit PathField's value processing
    assert field.get_prep_value("simple.path") == "simple.path"
    assert field.get_prep_value(["multi", "part", "path"]) == "multi.part.path"


def test_lquery_field_basic_validation():
    """Test that LqueryField accepts valid lquery patterns."""
    from django.db import models

    class TestModel(models.Model):
        pattern = LqueryField()

        class Meta:
            app_label = 'tests'

    # Valid lquery patterns should not raise ValidationError
    valid_patterns = [
        "simple.path",
        "*.wildcard.path",
        "path.*.with.wildcard",
        "f63969a8-536f-4c80-a0a3-fafdb53cb7cf.*"
    ]

    for pattern in valid_patterns:
        instance = TestModel(pattern=pattern)
        instance.full_clean()  # Should not raise


def test_lquery_pattern_matching(db):
    """Test basic lquery pattern matching with existing Taxonomy model."""
    # Create some test data using the existing Taxonomy model
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR Department")
    Taxonomy.objects.create(path="tenant_a.departments.finance", name="Finance Department")
    Taxonomy.objects.create(path="tenant_b.projects.alpha", name="Project Alpha")
    Taxonomy.objects.create(path="shared.public.docs", name="Public Documentation")

    # Test basic pattern matching
    hr_matches = Taxonomy.objects.filter(path__match="tenant_a.departments.*")
    assert hr_matches.count() == 2

    # Test wildcard pattern
    tenant_a_matches = Taxonomy.objects.filter(path__match="tenant_a.*")
    assert tenant_a_matches.count() == 2


def test_lquery_array_contains_lookup(db):
    """Test the key feature: contains lookup with array of lquery patterns."""
    # Create test data
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.projects.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    # Test array of patterns with contains lookup
    patterns = [
        "tenant_a.departments.*",  # HR department
        "shared.public.*",         # Public docs
    ]

    output_field = ArrayField(base_field=LqueryField())

    matching = Taxonomy.objects.filter(
        path__contains=Value(patterns, output_field=output_field)
    )

    # Should match HR and public docs (2 items)
    assert matching.count() == 2

    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Docs" in matched_names

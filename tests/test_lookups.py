import pytest
from taxonomy.models import Taxonomy

pytestmark = pytest.mark.django_db


def test_lookups_pattern_matching():
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


def test_lookups_contains():
    """Test the key feature: contains lookup with array of lquery patterns."""
    # Create test data
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.projects.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    # Test array of patterns with contains lookup
    patterns = [
        "tenant_a.departments.*",  # HR department
        "shared.public.*",  # Public docs
    ]

    matching = Taxonomy.objects.filter(path__contains=patterns)

    # Should match HR and public docs (2 items)
    assert matching.count() == 2

    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Docs" in matched_names


def test_lookups_contains_with_single_value():
    """Test the contains lookup with a single value."""
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.projects.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    matching = Taxonomy.objects.filter(path__contains=["tenant_a.*"])
    assert matching.count() == 2
    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Alpha Project" in matched_names


def test_lookups_contains_invalid_value():
    """Test the contains lookup with an invalid value."""
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.projects.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    with pytest.raises(TypeError):
        Taxonomy.objects.filter(path__contains="tenant_a.*")


def test_lookups_ancestors():
    """Test the ancestors lookup."""
    Taxonomy.objects.create(path="tenant_a", name="Tenant A")
    Taxonomy.objects.create(path="tenant_a.departments", name="Departments")
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    matching = Taxonomy.objects.filter(path__ancestors="tenant_a.departments")
    assert matching.count() == 2
    matched_names = set(item.name for item in matching)
    assert "Tenant A" in matched_names
    assert "Departments" in matched_names


def test_lookups_descendants():
    """Test the descendants lookup."""
    Taxonomy.objects.create(path="tenant_a", name="Tenant A")
    Taxonomy.objects.create(path="tenant_a.departments", name="Departments")
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    matching = Taxonomy.objects.filter(path__descendants="tenant_a.departments")

    assert matching.count() == 3
    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Alpha Project" in matched_names
    assert "Departments" in matched_names


def test_lookups_exact():
    """Test the exact lookup."""
    Taxonomy.objects.create(path="tenant_a", name="Tenant A")
    Taxonomy.objects.create(path="tenant_a.departments", name="Departments")
    Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    matching = Taxonomy.objects.filter(path__exact="tenant_a.departments.hr")
    assert matching.count() == 1
    assert "HR" == matching.first().name

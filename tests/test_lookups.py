import pytest
from tests.taxonomy.models import Taxonomy

pytestmark = pytest.mark.django_db


def test_lookups_pattern_matching():
    """Test basic lquery pattern matching with existing Taxonomy model."""
    # Create some test data using the existing Taxonomy model
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    # Test basic pattern matching
    hr_matches = Taxonomy.t_objects.filter(path__match=f"{b.path}.*")
    assert hr_matches.count() == 3

    # Test wildcard pattern
    tenant_a_matches = Taxonomy.t_objects.filter(path__match=f"*.{b.label()}.*")
    assert tenant_a_matches.count() == 3


def test_lookups_contains():
    """Test the key feature: contains lookup with array of lquery patterns."""
    # Create test data
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    # Test array of patterns with contains lookup
    patterns = [
        f"*.{c.label()}",
        f"{e.label()}",
    ]

    matching = Taxonomy.t_objects.filter(path__contains=patterns)

    # Should match HR, and Engineering (2 items)
    assert matching.count() == 2

    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Engineering" in matched_names


def test_lookups_contains_with_single_value():
    """Test the contains lookup with a single value."""
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    matching = Taxonomy.t_objects.filter(path__contains=[f"{b.path}.*"])
    assert matching.count() == 3
    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Alpha Project" in matched_names


def test_lookups_contains_invalid_value():
    """Test the contains lookup with an invalid value."""
    Taxonomy.t_objects.create(path="tenant_a.departments.hr", name="HR")
    Taxonomy.t_objects.create(path="tenant_a.projects.alpha", name="Alpha Project")
    Taxonomy.t_objects.create(path="tenant_b.departments.eng", name="Engineering")
    Taxonomy.t_objects.create(path="shared.public.docs", name="Docs")

    msg = "Contains lookup requires a list or tuple of values"
    with pytest.raises(TypeError, match=msg):
        Taxonomy.t_objects.filter(path__contains="tenant_a.*")


def test_lookups_ancestors():
    """Test the ancestors lookup."""
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    matching = Taxonomy.t_objects.filter(path__ancestors=b.path)
    assert matching.count() == 2
    matched_names = set(item.name for item in matching)
    assert "Tenant A" in matched_names
    assert "Departments" in matched_names


def test_lookups_descendants():
    """Test the descendants lookup."""
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    matching = Taxonomy.t_objects.filter(path__descendants=b.path)

    assert matching.count() == 3
    matched_names = set(item.name for item in matching)
    assert "HR" in matched_names
    assert "Alpha Project" in matched_names
    assert "Departments" in matched_names


def test_lookups_exact():
    """Test the exact lookup."""
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    matching = Taxonomy.t_objects.filter(path__exact=c.path)
    assert matching.count() == 1
    assert "HR" == matching.first().name


def test_lookups_depth():
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")

    assert len(Taxonomy.t_objects.filter(path__depth=1)) == 2
    assert len(Taxonomy.t_objects.filter(path__depth=3)) == 2

    assert "Tenant A" in set(t.name for t in Taxonomy.t_objects.filter(path__depth=1))

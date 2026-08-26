import pytest

from django_ltree.managers import TreeManager
from django_ltree.utils import pad_path_labels
from tests.taxonomy.models import LegacyTaxonomy, Taxonomy, TaxonomyName

# Taxonomy uses a BigAutoField primary key, so labels resolve to 19 digits
WIDTH = 19


def test_resolve_label_width():
    assert Taxonomy.t_objects.resolve_label_width() == WIDTH  # BigAutoField, auto
    assert TaxonomyName.t_objects.resolve_label_width() is None  # TextField, auto
    assert LegacyTaxonomy.t_objects.resolve_label_width() is None  # opted out

    assert TreeManager(label_width=4).resolve_label_width() == 4


def test_format_label():
    manager = TreeManager(label_width=4)
    assert manager.format_label(7) == "0007"
    assert manager.format_label("abc") == "abc"
    assert manager.format_label("a1") == "a1"

    with pytest.raises(ValueError, match="label_width"):
        manager.format_label(12345)

    unpadded = TreeManager(label_width=None)
    assert unpadded.format_label(7) == "7"


def test_padded_labels_sort_numerically(db):
    for pk in (2, 9, 10, 100):
        Taxonomy.t_objects.create(id=pk, name="node {}".format(pk))

    assert [obj.pk for obj in Taxonomy.t_objects.roots()] == [2, 9, 10, 100]


def test_padded_paths(db):
    root = Taxonomy.t_objects.create(id=2, name="root")
    child = Taxonomy.t_objects.create_child(parent=root, id=10, name="child")

    assert str(root.path) == "2".zfill(WIDTH)
    assert str(child.path) == "{}.{}".format("2".zfill(WIDTH), "10".zfill(WIDTH))


def test_lookups_accept_unpadded_values(db):
    root = Taxonomy.t_objects.create(id=2, name="root")
    child = Taxonomy.t_objects.create_child(parent=root, id=10, name="child")

    for node in (root, root.path, "2", [2]):
        assert child in Taxonomy.t_objects.descendants_of(node)
        assert child in Taxonomy.t_objects.children(node)

    assert root in Taxonomy.t_objects.ancestors_of("2.10")


def test_label_width_survives_queryset_chaining(db):
    root = Taxonomy.t_objects.create(id=2, name="root")
    child = Taxonomy.t_objects.create_child(parent=root, id=10, name="child")

    qs = Taxonomy.t_objects.filter(name="child").descendants_of("2")
    assert child in qs


def test_create_child_accepts_unpadded_string_parent(db):
    Taxonomy.t_objects.create(id=2, name="root")
    child = Taxonomy.t_objects.create_child(parent="2", id=10, name="child")

    assert str(child.path) == "{}.{}".format("2".zfill(WIDTH), "10".zfill(WIDTH))


def test_change_parent_accepts_unpadded_string(db):
    a = Taxonomy.t_objects.create(id=2, name="a")
    b = Taxonomy.t_objects.create(id=10, name="b")

    b.change_parent("2")
    b.refresh_from_db()

    assert str(b.path) == "{}.{}".format("2".zfill(WIDTH), "10".zfill(WIDTH))
    assert b.parent() == a


def test_legacy_unpadded_labels_sort_as_text(db):
    for pk in (2, 9, 10, 100):
        LegacyTaxonomy.t_objects.create(id=pk, name="node {}".format(pk))

    # label_width=None keeps the pre-0.8 behavior: labels compare as text
    assert [obj.pk for obj in LegacyTaxonomy.t_objects.roots()] == [10, 100, 2, 9]
    assert str(LegacyTaxonomy.t_objects.get(pk=2).path) == "2"


def test_pad_path_labels_migration_helper(db):
    for pk in (2, 9, 10, 100):
        LegacyTaxonomy.t_objects.create(id=pk, name="node {}".format(pk))
    LegacyTaxonomy.t_objects.create_child(
        parent=LegacyTaxonomy.t_objects.get(pk=2), id=101, name="child"
    )

    updated = pad_path_labels(LegacyTaxonomy, label_width=WIDTH)
    assert updated == 5

    assert [obj.pk for obj in LegacyTaxonomy.t_objects.roots()] == [2, 9, 10, 100]

    child = LegacyTaxonomy.t_objects.get(pk=101)
    assert str(child.path) == "{}.{}".format("2".zfill(WIDTH), "101".zfill(WIDTH))
    assert [a.pk for a in child.ancestors()] == [2, 101]

import pytest
from tests.conftest import create_tree
from tests.taxonomy.models import Taxonomy


def test_create(taxonomy_tree):
    assert Taxonomy.t_objects.count() != 0


def test_roots(taxonomy_tree):
    roots = Taxonomy.t_objects.roots().values_list("name", flat=True)
    assert set(roots) == {"Bacteria", "Plantae", "Animalia"}


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Animalia", ["Chordata"]),
        ("Mammalia", ["Carnivora", "Pilosa"]),
        ("Reptilia", ["Squamata"]),
        ("Pogona", ["Pogona barbata", "Pogona minor", "Pogona vitticeps"]),
    ],
)
def test_children(taxonomy_tree, name, expected):
    children = taxonomy_tree(name).children().values_list("name", flat=True)
    assert set(children) == set(expected)


def test_children_accepts_instance_or_path(taxonomy_tree):
    mammalia = taxonomy_tree("Mammalia")

    by_instance = set(Taxonomy.t_objects.children(mammalia).values_list("name", flat=True))
    by_path = set(Taxonomy.t_objects.children(mammalia.path).values_list("name", flat=True))
    by_string = set(Taxonomy.t_objects.children(str(mammalia.path)).values_list("name", flat=True))

    assert by_instance == by_path == by_string == {"Carnivora", "Pilosa"}


def test_descendants_of_excludes_self_by_default(taxonomy_tree):
    carnivora = taxonomy_tree("Carnivora")

    descendants = Taxonomy.t_objects.descendants_of(carnivora)
    assert carnivora not in descendants
    assert descendants.count() == 14

    with_self = Taxonomy.t_objects.descendants_of(carnivora, include_self=True)
    assert carnivora in with_self
    assert with_self.count() == 15


@pytest.mark.parametrize(
    "max_depth, expected",
    [
        (1, {"Canidae", "Feliformia"}),
        (2, {"Canidae", "Canis", "Urocyon", "Feliformia", "Felidae"}),
    ],
)
def test_descendants_of_max_depth(taxonomy_tree, max_depth, expected):
    carnivora = taxonomy_tree("Carnivora")
    names = Taxonomy.t_objects.descendants_of(carnivora, max_depth=max_depth).values_list(
        "name", flat=True
    )
    assert set(names) == expected


def test_descendants_of_invalid_arguments(taxonomy_tree):
    carnivora = taxonomy_tree("Carnivora")

    with pytest.raises(ValueError):
        Taxonomy.t_objects.descendants_of(carnivora, max_depth=0)

    with pytest.raises(ValueError):
        Taxonomy.t_objects.descendants_of([])


def test_ancestors_of(taxonomy_tree):
    canis = taxonomy_tree("Canis")

    ancestors = Taxonomy.t_objects.ancestors_of(canis).values_list("name", flat=True)
    assert list(ancestors) == ["Animalia", "Chordata", "Mammalia", "Carnivora", "Canidae"]

    with_self = Taxonomy.t_objects.ancestors_of(canis, include_self=True).values_list(
        "name", flat=True
    )
    assert list(with_self) == ["Animalia", "Chordata", "Mammalia", "Carnivora", "Canidae", "Canis"]


def test_label(taxonomy_tree):
    for item in Taxonomy.t_objects.all():
        label = item.label()
        assert label.isalnum()
        assert str(item.path).endswith(label)


def test_add_child(db):
    create_tree("test data\nanother data")

    test: Taxonomy = Taxonomy.t_objects.get(name="test data")
    test.add_child(name="this data")

    data: Taxonomy = Taxonomy.t_objects.get(name="this data")

    assert data.parent() == test


@pytest.mark.parametrize(
    "name, expected",
    [
        (
            "Canis lupus",
            ["Animalia", "Chordata", "Mammalia", "Carnivora", "Canidae", "Canis", "Canis lupus"],
        ),
        ("Bacteria", ["Bacteria"]),
        ("Chordata", ["Animalia", "Chordata"]),
    ],
)
def test_ancestors(taxonomy_tree, name, expected):
    ancestors = taxonomy_tree(name).ancestors().values_list("name", flat=True)
    assert list(ancestors) == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        (
            "Canidae",
            [
                "Canidae",
                "Canis",
                "Canis lupus",
                "Canis rufus",
                "Urocyon",
                "Urocyon cinereoargenteus",
            ],
        ),
        ("Bradypus tridactylus", ["Bradypus tridactylus"]),
        ("Pogona", ["Pogona", "Pogona barbata", "Pogona minor", "Pogona vitticeps"]),
    ],
)
def test_descendants(taxonomy_tree, name, expected):
    descendants = taxonomy_tree(name).descendants().values_list("name", flat=True)
    assert set(descendants) == set(expected)


@pytest.mark.parametrize(
    "name, expected", [("Feliformia", "Carnivora"), ("Plantae", None), ("Pogona minor", "Pogona")]
)
def test_parent(taxonomy_tree, name, expected):
    parent = taxonomy_tree(name).parent()
    assert getattr(parent, "name", None) == expected


@pytest.mark.parametrize(
    "name, expected",
    [("Carnivora", ["Pilosa"]), ("Pogona vitticeps", ["Pogona minor", "Pogona barbata"])],
)
def test_siblings(taxonomy_tree, name, expected):
    siblings = taxonomy_tree(name).siblings().values_list("name", flat=True)
    assert set(siblings) == set(expected)


def test_slicing(taxonomy_tree):
    qs = Taxonomy.t_objects.all()
    assert qs[:3].count() == 3


def test_change_parent(taxonomy_tree):
    carnivora: Taxonomy = taxonomy_tree("Carnivora")
    pilosa: Taxonomy = taxonomy_tree("Pilosa")
    carnivora.change_parent(pilosa)

    assert carnivora in pilosa.children()
    assert set(pilosa.descendants()).issuperset(set(carnivora.descendants()))

    carnivora.refresh_from_db()
    child = carnivora.children().first()

    assert carnivora.path[:-1] == pilosa.path
    assert child.path[:-2] == pilosa.path


def test_make_root(taxonomy_tree):
    carnivora: Taxonomy = taxonomy_tree("Carnivora")

    assert carnivora.parent()
    assert len(carnivora.descendants()) == 15

    carnivora.make_root()
    carnivora.refresh_from_db()

    assert carnivora.parent() is None
    assert len(carnivora.descendants()) == 15


def test_delete_cascade(taxonomy_tree):
    carnivora: Taxonomy = taxonomy_tree("Carnivora")
    canidae: Taxonomy = taxonomy_tree("Canidae")

    carnivora.delete_cascade()
    canidae = Taxonomy.t_objects.filter(name="Canidae").exists()

    assert not canidae


def test_delete_with_cascade_param(taxonomy_tree):
    carnivora: Taxonomy = taxonomy_tree("Carnivora")
    canidae: Taxonomy = taxonomy_tree("Canidae")

    carnivora.delete(cascade=True)
    canidae = Taxonomy.t_objects.filter(name="Canidae").exists()

    assert not canidae


def test_delete_no_cascade_with_parent(taxonomy_tree):
    carnivora: Taxonomy = taxonomy_tree("Carnivora")
    parent = carnivora.parent()
    canidae: Taxonomy = taxonomy_tree("Canidae")
    assert carnivora in canidae.ancestors()

    carnivora.delete()

    canidae.refresh_from_db()
    assert carnivora not in canidae.ancestors()
    assert parent == canidae.parent()


def test_delete_no_cascade_without_parent(taxonomy_tree):
    animalia: Taxonomy = taxonomy_tree("Animalia")
    parent = animalia.parent()

    assert parent is None

    chrodata: Taxonomy = taxonomy_tree("Chordata")
    des = list(chrodata.descendants())

    assert animalia in chrodata.ancestors()

    animalia.delete()
    chrodata.refresh_from_db()

    assert animalia not in chrodata.ancestors()
    assert chrodata.parent() is None
    assert list(chrodata.descendants()) == des


def test_get_root(taxonomy_tree):
    mammalia: Taxonomy = taxonomy_tree("Mammalia")

    root = mammalia.get_root()

    assert root.name == "Animalia"

    bacteria: Taxonomy = taxonomy_tree("Bacteria")

    root = bacteria.get_root()

    assert root.name == "Bacteria"

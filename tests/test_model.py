import pytest
from tests.taxonomy.models import Taxonomy

TEST_DATA = [
    {"name": "Bacteria"},
    {"name": "Plantae"},
    {
        "name": "Animalia",
        "sub": [
            {
                "name": "Chordata",
                "sub": [
                    {
                        "name": "Mammalia",
                        "sub": [
                            {
                                "name": "Carnivora",
                                "sub": [
                                    {
                                        "name": "Canidae",
                                        "sub": [
                                            {
                                                "name": "Canis",
                                                "sub": [
                                                    {"name": "Canis lupus"},
                                                    {"name": "Canis rufus"},
                                                ],
                                            },
                                            {
                                                "name": "Urocyon",
                                                "sub": [{"name": "Urocyon cinereoargenteus"}],
                                            },
                                        ],
                                    },
                                    {
                                        "name": "Feliformia",
                                        "sub": [
                                            {
                                                "name": "Felidae",
                                                "sub": [
                                                    {
                                                        "name": "Felinae",
                                                        "sub": [
                                                            {
                                                                "name": "Lynx",
                                                                "sub": [
                                                                    {"name": "Lynx lynx"},
                                                                    {"name": "Lynx rufus"},
                                                                ],
                                                            },
                                                            {
                                                                "name": "Puma",
                                                                "sub": [{"name": "Puma concolor"}],
                                                            },
                                                        ],
                                                    }
                                                ],
                                            }
                                        ],
                                    },
                                ],
                            },
                            {
                                "name": "Pilosa",
                                "sub": [
                                    {
                                        "name": "Folivora",
                                        "sub": [
                                            {
                                                "name": "Bradypodidae",
                                                "sub": [
                                                    {
                                                        "name": "Bradypus",
                                                        "sub": [{"name": "Bradypus tridactylus"}],
                                                    }
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "name": "Reptilia",
                        "sub": [
                            {
                                "name": "Squamata",
                                "sub": [
                                    {
                                        "name": "Iguania",
                                        "sub": [
                                            {
                                                "name": "Agamidae",
                                                "sub": [
                                                    {
                                                        "name": "Pogona",
                                                        "sub": [
                                                            {"name": "Pogona barbata"},
                                                            {"name": "Pogona minor"},
                                                            {"name": "Pogona vitticeps"},
                                                        ],
                                                    }
                                                ],
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    },
                ],
            }
        ],
    },
]


def create_objects(objects, parent):
    for obj in objects:
        created = Taxonomy.t_objects.create_child(parent, name=obj["name"])
        if "sub" in obj:
            create_objects(obj["sub"], created)


def create_test_data():
    create_objects(TEST_DATA, parent=None)


def test_create(db):
    create_test_data()
    assert Taxonomy.t_objects.count() != 0


def test_roots(db):
    create_test_data()
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
def test_children(db, name, expected):
    create_test_data()
    children = Taxonomy.t_objects.get(name=name).children().values_list("name", flat=True)
    assert set(children) == set(expected)


def test_children_accepts_instance_or_path(db):
    create_test_data()
    mammalia = Taxonomy.t_objects.get(name="Mammalia")

    by_instance = set(Taxonomy.t_objects.children(mammalia).values_list("name", flat=True))
    by_path = set(Taxonomy.t_objects.children(mammalia.path).values_list("name", flat=True))
    by_string = set(Taxonomy.t_objects.children(str(mammalia.path)).values_list("name", flat=True))

    assert by_instance == by_path == by_string == {"Carnivora", "Pilosa"}


def test_descendants_of_excludes_self_by_default(db):
    create_test_data()
    carnivora = Taxonomy.t_objects.get(name="Carnivora")

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
def test_descendants_of_max_depth(db, max_depth, expected):
    create_test_data()
    carnivora = Taxonomy.t_objects.get(name="Carnivora")
    names = Taxonomy.t_objects.descendants_of(carnivora, max_depth=max_depth).values_list(
        "name", flat=True
    )
    assert set(names) == expected


def test_descendants_of_invalid_arguments(db):
    create_test_data()
    carnivora = Taxonomy.t_objects.get(name="Carnivora")

    with pytest.raises(ValueError):
        Taxonomy.t_objects.descendants_of(carnivora, max_depth=0)

    with pytest.raises(ValueError):
        Taxonomy.t_objects.descendants_of([])


def test_ancestors_of(db):
    create_test_data()
    canis = Taxonomy.t_objects.get(name="Canis")

    ancestors = Taxonomy.t_objects.ancestors_of(canis).values_list("name", flat=True)
    assert list(ancestors) == ["Animalia", "Chordata", "Mammalia", "Carnivora", "Canidae"]

    with_self = Taxonomy.t_objects.ancestors_of(canis, include_self=True).values_list(
        "name", flat=True
    )
    assert list(with_self) == ["Animalia", "Chordata", "Mammalia", "Carnivora", "Canidae", "Canis"]


def test_label(db):
    create_test_data()
    for item in Taxonomy.t_objects.all():
        label = item.label()
        assert label.isalnum()
        assert str(item.path).endswith(label)


def test_add_child(db):
    create_objects([{"name": "test data"}, {"name": "another data"}], parent=None)

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
def test_ancestors(db, name, expected):
    create_test_data()
    ancestors = Taxonomy.t_objects.get(name=name).ancestors().values_list("name", flat=True)
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
def test_descendants(db, name, expected):
    create_test_data()
    descendants = Taxonomy.t_objects.get(name=name).descendants().values_list("name", flat=True)
    assert set(descendants) == set(expected)


@pytest.mark.parametrize(
    "name, expected", [("Feliformia", "Carnivora"), ("Plantae", None), ("Pogona minor", "Pogona")]
)
def test_parent(db, name, expected):
    create_test_data()
    parent = Taxonomy.t_objects.get(name=name).parent()
    assert getattr(parent, "name", None) == expected


@pytest.mark.parametrize(
    "name, expected",
    [("Carnivora", ["Pilosa"]), ("Pogona vitticeps", ["Pogona minor", "Pogona barbata"])],
)
def test_siblings(db, name, expected):
    create_test_data()
    siblings = Taxonomy.t_objects.get(name=name).siblings().values_list("name", flat=True)
    assert set(siblings) == set(expected)


def test_slicing(db):
    create_test_data()
    qs = Taxonomy.t_objects.all()
    assert qs[:3].count() == 3


def test_change_parent(db):
    create_test_data()
    carnivora: Taxonomy = Taxonomy.t_objects.get(name="Carnivora")
    pilosa: Taxonomy = Taxonomy.t_objects.get(name="Pilosa")
    carnivora.change_parent(pilosa)

    assert carnivora in pilosa.children()
    assert set(pilosa.descendants()).issuperset(set(carnivora.descendants()))

    carnivora.refresh_from_db()
    child = carnivora.children().first()

    assert carnivora.path[:-1] == pilosa.path
    assert child.path[:-2] == pilosa.path


def test_make_root(db):
    create_test_data()
    carnivora: Taxonomy = Taxonomy.t_objects.get(name="Carnivora")

    assert carnivora.parent()
    assert len(carnivora.descendants()) == 15

    carnivora.make_root()
    carnivora.refresh_from_db()

    assert carnivora.parent() is None
    assert len(carnivora.descendants()) == 15


def test_delete_cascade(db):
    create_test_data()
    carnivora: Taxonomy = Taxonomy.t_objects.get(name="Carnivora")
    canidae: Taxonomy = Taxonomy.t_objects.get(name="Canidae")

    carnivora.delete_cascade()
    canidae: Taxonomy = Taxonomy.t_objects.filter(name="Canidae").exists()

    assert not canidae


def test_delete_with_cascade_param(db):
    create_test_data()
    carnivora: Taxonomy = Taxonomy.t_objects.get(name="Carnivora")
    canidae: Taxonomy = Taxonomy.t_objects.get(name="Canidae")

    carnivora.delete(cascade=True)
    canidae: Taxonomy = Taxonomy.t_objects.filter(name="Canidae").exists()

    assert not canidae


def test_delete_no_cascade_with_parent(db):
    create_test_data()
    carnivora: Taxonomy = Taxonomy.t_objects.get(name="Carnivora")
    parent = carnivora.parent()
    canidae: Taxonomy = Taxonomy.t_objects.get(name="Canidae")
    assert carnivora in canidae.ancestors()

    carnivora.delete()

    canidae.refresh_from_db()
    assert carnivora not in canidae.ancestors()
    assert parent == canidae.parent()


def test_delete_no_cascade_without_parent(db):
    create_test_data()
    animalia: Taxonomy = Taxonomy.t_objects.get(name="Animalia")
    parent = animalia.parent()

    assert parent is None

    chrodata: Taxonomy = Taxonomy.t_objects.get(name="Chordata")
    des = list(chrodata.descendants())

    assert animalia in chrodata.ancestors()

    animalia.delete()
    chrodata.refresh_from_db()

    assert animalia not in chrodata.ancestors()
    assert chrodata.parent() is None
    assert list(chrodata.descendants()) == des


def test_get_root(db):
    create_test_data()
    mammalia: Taxonomy = Taxonomy.t_objects.get(name="Mammalia")

    root = mammalia.get_root()

    assert root.name == "Animalia"

    bacteria: Taxonomy = Taxonomy.t_objects.get(name="Bacteria")

    root = bacteria.get_root()

    assert root.name == "Bacteria"

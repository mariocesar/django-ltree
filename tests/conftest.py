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


@pytest.fixture
def taxonomy_tree(db):
    """Full taxonomy tree built from TEST_DATA; returns a node getter by name."""
    create_objects(TEST_DATA, parent=None)
    return lambda name: Taxonomy.t_objects.get(name=name)

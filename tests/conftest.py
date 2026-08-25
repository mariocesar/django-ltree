import pytest
from tests.taxonomy.models import Taxonomy

TEST_DATA = """
Bacteria
Plantae
Animalia.Chordata.Mammalia.Carnivora.Canidae.Canis.Canis lupus
Animalia.Chordata.Mammalia.Carnivora.Canidae.Canis.Canis rufus
Animalia.Chordata.Mammalia.Carnivora.Canidae.Urocyon.Urocyon cinereoargenteus
Animalia.Chordata.Mammalia.Carnivora.Feliformia.Felidae.Felinae.Lynx.Lynx lynx
Animalia.Chordata.Mammalia.Carnivora.Feliformia.Felidae.Felinae.Lynx.Lynx rufus
Animalia.Chordata.Mammalia.Carnivora.Feliformia.Felidae.Felinae.Puma.Puma concolor
Animalia.Chordata.Mammalia.Pilosa.Folivora.Bradypodidae.Bradypus.Bradypus tridactylus
Animalia.Chordata.Reptilia.Squamata.Iguania.Agamidae.Pogona.Pogona barbata
Animalia.Chordata.Reptilia.Squamata.Iguania.Agamidae.Pogona.Pogona minor
Animalia.Chordata.Reptilia.Squamata.Iguania.Agamidae.Pogona.Pogona vitticeps
"""


def create_tree(text):
    nodes = {}
    for line in text.strip().splitlines():
        path = ()
        for name in line.split("."):
            path += (name,)
            if path not in nodes:
                nodes[path] = Taxonomy.t_objects.create_child(nodes.get(path[:-1]), name=name)


@pytest.fixture
def taxonomy_tree(db):
    """Full taxonomy tree built from TEST_DATA; returns a node getter by name."""
    create_tree(TEST_DATA)
    return lambda name: Taxonomy.t_objects.get(name=name)

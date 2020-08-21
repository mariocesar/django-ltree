import pytest

from taxonomy.models import Taxonomy


TEST_DATA = [
    {'name': 'Bacteria'},
    {'name': 'Plantae'},
    {
        'name': 'Animalia',
        'sub': [
            {
                'name': 'Chordata',
                'sub': [
                    {
                        'name': 'Mammalia',
                        'sub': [
                            {
                                'name': 'Carnivora',
                                'sub': [
                                    {
                                        'name': 'Canidae',
                                        'sub': [
                                            {
                                                'name': 'Canis',
                                                'sub': [{'name': 'Canis lupus'}, {'name': 'Canis rufus'}]
                                            },
                                            {
                                                'name': 'Urocyon',
                                                'sub': [{'name': 'Urocyon cinereoargenteus'}]
                                            }
                                        ]
                                    },
                                    {
                                        'name': 'Feliformia',
                                        'sub': [
                                            {
                                                'name': 'Felidae',
                                                'sub': [
                                                    {
                                                        'name': 'Felinae',
                                                        'sub': [
                                                            {
                                                                'name': 'Lynx',
                                                                'sub': [{'name': 'Lynx lynx'}, {'name': 'Lynx rufus'}]
                                                            },
                                                            {
                                                                'name': 'Puma',
                                                                'sub': [{'name': 'Puma concolor'}]
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                'name': 'Pilosa',
                                'sub': [
                                    {
                                        'name': 'Folivora',
                                        'sub': [
                                            {
                                                'name': 'Bradypodidae',
                                                'sub': [
                                                    {
                                                        'name': 'Bradypus',
                                                        'sub': [{'name': 'Bradypus tridactylus'}]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'Reptilia',
                        'sub': [
                            {
                                'name': 'Squamata',
                                'sub': [
                                    {
                                        'name': 'Iguania',
                                        'sub': [
                                            {
                                                'name': 'Agamidae',
                                                'sub': [
                                                    {
                                                        'name': 'Pogona',
                                                        'sub': [
                                                            {'name': 'Pogona barbata'},
                                                            {'name': 'Pogona minor'},
                                                            {'name': 'Pogona vitticeps'}
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
]


def create_objects(objects, parent):
    for obj in objects:
        created = Taxonomy.objects.create_child(parent, name=obj['name'])
        if 'sub' in obj:
            create_objects(obj['sub'], created)


def create_test_data():
    create_objects(TEST_DATA, parent=None)


def test_create(db):
    create_test_data()
    assert Taxonomy.objects.count() != 0


def test_roots(db):
    create_test_data()
    roots = Taxonomy.objects.roots().values_list('name', flat=True)
    assert set(roots) == set(['Bacteria', 'Plantae', 'Animalia'])


@pytest.mark.parametrize(
    'name, expected', [
        ('Animalia', ['Chordata']),
        ('Mammalia', ['Carnivora', 'Pilosa']),
        ('Reptilia', ['Squamata']),
        ('Pogona', ['Pogona barbata', 'Pogona minor', 'Pogona vitticeps'])
    ]
)
def test_children(db, name, expected):
    create_test_data()
    children = Taxonomy.objects.get(name=name).children().values_list('name', flat=True)
    assert set(children) == set(expected)


def test_label(db):
    create_test_data()
    for item in Taxonomy.objects.all():
        label = item.label()
        assert label.isalnum()
        assert str(item.path).endswith(label)


@pytest.mark.parametrize(
    'name, expected', [
        ('Canis lupus', ['Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Canidae', 'Canis', 'Canis lupus']),
        ('Bacteria', ['Bacteria']),
        ('Chordata', ['Animalia', 'Chordata'])
    ]
)
def test_ancestors(db, name, expected):
    create_test_data()
    ancestors = Taxonomy.objects.get(name=name).ancestors().values_list('name', flat=True)
    assert list(ancestors) == expected


@pytest.mark.parametrize(
    'name, expected', [
        ('Canidae', ['Canidae', 'Canis', 'Canis lupus', 'Canis rufus', 'Urocyon', 'Urocyon cinereoargenteus']),
        ('Bradypus tridactylus', ['Bradypus tridactylus']),
        ('Pogona', ['Pogona', 'Pogona barbata', 'Pogona minor', 'Pogona vitticeps'])
    ]
)
def test_descendants(db, name, expected):
    create_test_data()
    descendants = Taxonomy.objects.get(name=name).descendants().values_list('name', flat=True)
    assert set(descendants) == set(expected)


@pytest.mark.parametrize(
    'name, expected', [
        ('Feliformia', 'Carnivora'),
        ('Plantae', None),
        ('Pogona minor', 'Pogona')
    ]
)
def test_parent(db, name, expected):
    create_test_data()
    parent = Taxonomy.objects.get(name=name).parent()
    assert getattr(parent, 'name', None) == expected


@pytest.mark.parametrize(
    'name, expected', [
        ('Carnivora', ['Pilosa']),
        ('Pogona vitticeps', ['Pogona minor', 'Pogona barbata'])
    ]
)
def test_siblings(db, name, expected):
    create_test_data()
    siblings = Taxonomy.objects.get(name=name).siblings().values_list('name', flat=True)
    assert set(siblings) == set(expected)


def test_slicing(db):
    create_test_data()
    qs = Taxonomy.objects.all()
    assert qs[:3].count() == 3

from taxonomy.models import Taxonomy


TEST_DATA = [
    {
        'name': 'Bacteria'
    },
    {
        'name': 'Plantae',
    },
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
                                                'sub': [
                                                    {'name': 'Canis lupus'},
                                                    {'name': 'Canis rufus'}
                                                ]
                                            },
                                            {
                                                'name': 'Urocyon',
                                                'sub': [
                                                    {'name': 'Urocyon cinereoargenteus'}
                                                ]
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
                                                                'name': 'Puma',
                                                                'sub': [
                                                                    {'name': 'Puma concolor'}
                                                                ]
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
                                                        'sub': [
                                                            {'name': 'Bradypus tridactylus'}
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


def test_children(db):
    create_test_data()
    children = Taxonomy.objects.get(name='Mammalia').children().values_list('name', flat=True)
    assert set(children) == set(['Carnivora', 'Pilosa'])


def test_label(db):
    create_test_data()
    for item in Taxonomy.objects.all():
        label = item.label()
        assert label.isalnum()
        assert str(item.path).endswith(label)

def test_ancestors(db):
    create_test_data()
    ancestors = Taxonomy.objects.get(name='Canis lupus').ancestors().values_list('name', flat=True)
    assert list(ancestors) == ['Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Canidae', 'Canis']


def test_descendants(db):
    create_test_data()
    descendants = Taxonomy.objects.get(name='Canidae').descendants().values_list('name', flat=True)
    assert set(descendants) == set(['Canis', 'Canis lupus', 'Canis rufus', 'Urocyon', 'Urocyon cinereoargenteus'])


def test_parent(db):
    create_test_data()
    parent = Taxonomy.objects.get(name='Feliformia').parent()
    assert parent.name == 'Carnivora'


def test_siblings(db):
    create_test_data()
    siblings = Taxonomy.objects.get(name='Carnivora').siblings().values_list('name', flat=True)
    assert set(siblings) == set(['Pilosa'])
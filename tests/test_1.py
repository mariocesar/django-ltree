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

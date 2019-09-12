from django.test import TestCase

from categories.models import Taxonomy

DATA = [
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


class TaxonomyTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls._create_objects(DATA, parent=None)

    @classmethod
    def _create_objects(cls, objects, parent):
        for obj in objects:
            created = Taxonomy.objects.create_child(parent, name=obj['name'])
            if 'sub' in obj:
                cls._create_objects(obj['sub'], created)

    def test_roots(self):
        roots = Taxonomy.objects.roots().values_list('name', flat=True)
        self.assertItemsEqual(roots, ['Bacteria', 'Plantae', 'Animalia'])

    def test_children(self):
        children = Taxonomy.objects.get(name='Mammalia').children().values_list('name', flat=True)
        self.assertItemsEqual(children, ['Carnivora', 'Pilosa'])

    def test_label(self):
        for item in Taxonomy.objects.all():
            label = item.label()
            self.assertTrue(label.isalnum())
            self.assertTrue(str(item.path).endswith(label))

    def test_ancestors(self):
        ancestors = Taxonomy.objects.get(name='Canis lupus').ancestors().values_list('name', flat=True)
        self.assertListEqual(list(ancestors), ['Animalia', 'Chordata', 'Mammalia', 'Carnivora', 'Canidae', 'Canis'])

    def test_descendants(self):
        descendants = Taxonomy.objects.get(name='Canidae').descendants().values_list('name', flat=True)
        self.assertItemsEqual(descendants,
                              ['Canis', 'Canis lupus', 'Canis rufus', 'Urocyon', 'Urocyon cinereoargenteus'])

    def test_parent(self):
        parent = Taxonomy.objects.get(name='Feliformia').parent()
        self.assertEqual(parent.name, 'Carnivora')

    def test_siblings(self):
        siblings = Taxonomy.objects.get(name='Carnivora').siblings().values_list('name', flat=True)
        self.assertItemsEqual(siblings, ['Pilosa'])

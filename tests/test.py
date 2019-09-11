from taxonomy.models import Taxonomy


def test_create_child(db):
    obj = Taxonomy.objects.create_child(name='Bacteria')
    assert obj.name == 'Bacteria'

from django.db.models import F, Value

from django_ltree.functions import Subpath
from django_ltree.lookups import NLevel
from tests.taxonomy.models import Taxonomy


def test_subpath(db):
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    data = Taxonomy.t_objects.filter(path=Subpath(F("path"), 0, 1), path__descendants=a.path)
    assert len(data) == 1
    assert data.get() == a

    data = Taxonomy.t_objects.filter(path=Subpath(F("path"), 0), path__descendants=a.path)
    assert len(data) == 4
    assert d in data
    assert e not in data


def test_nlevel(db):
    a = Taxonomy.t_objects.create(name="Tenant A")
    b = Taxonomy.t_objects.create_child(parent=a, name="Departments")
    c = Taxonomy.t_objects.create_child(parent=b, name="HR")
    d = Taxonomy.t_objects.create_child(parent=b, name="Alpha Project")
    e = Taxonomy.t_objects.create(name="Engineering")
    f = Taxonomy.t_objects.create(name="Docs")

    data = Taxonomy.t_objects.filter(path__depth=NLevel(Value(str(b.path))))
    assert len(data) == 1

    data = Taxonomy.t_objects.filter(path__depth=NLevel(Value(str(c.path))))
    assert len(data) == 2

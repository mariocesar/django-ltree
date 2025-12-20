from django.db.models import F, Value

from django_ltree.functions import Subpath
from django_ltree.lookups import NLevel
from tests.taxonomy.models import Taxonomy


def test_subpath(db):
    a = Taxonomy.t_objects.create(path="tenant_a", name="Tenant A")
    b = Taxonomy.t_objects.create(path="tenant_a.departments", name="Departments")
    c = Taxonomy.t_objects.create(path="tenant_a.departments.hr", name="HR")
    d = Taxonomy.t_objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    e = Taxonomy.t_objects.create(path="tenant_b.departments.eng", name="Engineering")
    f = Taxonomy.t_objects.create(path="shared.public.docs", name="Docs")

    data = Taxonomy.t_objects.filter(path=Subpath(F("path"), 0, 1), path__descendants=a.path)
    assert len(data) == 1
    assert data.get() == a

    data = Taxonomy.t_objects.filter(path=Subpath(F("path"), 0), path__descendants=a.path)
    assert len(data) == 4
    assert d in data
    assert e not in data


def test_nlevel(db):
    a = Taxonomy.t_objects.create(path="tenant_a", name="Tenant A")
    b = Taxonomy.t_objects.create(path="tenant_a.departments", name="Departments")
    c = Taxonomy.t_objects.create(path="tenant_a.departments.hr", name="HR")
    d = Taxonomy.t_objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    e = Taxonomy.t_objects.create(path="tenant_b.departments.eng", name="Engineering")
    f = Taxonomy.t_objects.create(path="shared.public", name="Public")
    f = Taxonomy.t_objects.create(path="shared.public.docs", name="Docs")

    data = Taxonomy.t_objects.filter(path__depth=NLevel(Value(str(b.path))))
    assert len(data) == 2

    data = Taxonomy.t_objects.filter(path__depth=NLevel(Value(str(c.path))))
    assert len(data) == 4

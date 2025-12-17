from django.db.models import F, Value

from django_ltree.functions import Subpath
from django_ltree.lookups import NLevel
from tests.taxonomy.models import Taxonomy


def test_subpath(db):
    a = Taxonomy.objects.create(path="tenant_a", name="Tenant A")
    b = Taxonomy.objects.create(path="tenant_a.departments", name="Departments")
    c = Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    d = Taxonomy.objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    e = Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    f = Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    data = Taxonomy.objects.filter(path=Subpath(F("path"), 0, 1), path__descendants=a.path)
    assert len(data) == 1
    assert data.get() == a

    data = Taxonomy.objects.filter(path=Subpath(F("path"), 0), path__descendants=a.path)
    assert len(data) == 4
    assert d in data
    assert e not in data


def test_nlevel(db):
    a = Taxonomy.objects.create(path="tenant_a", name="Tenant A")
    b = Taxonomy.objects.create(path="tenant_a.departments", name="Departments")
    c = Taxonomy.objects.create(path="tenant_a.departments.hr", name="HR")
    d = Taxonomy.objects.create(path="tenant_a.departments.alpha", name="Alpha Project")
    e = Taxonomy.objects.create(path="tenant_b.departments.eng", name="Engineering")
    f = Taxonomy.objects.create(path="shared.public", name="Public")
    f = Taxonomy.objects.create(path="shared.public.docs", name="Docs")

    data = Taxonomy.objects.filter(path__depth=NLevel(Value(str(b.path))))
    assert len(data) == 2

    data = Taxonomy.objects.filter(path__depth=NLevel(Value(str(c.path))))
    assert len(data) == 4

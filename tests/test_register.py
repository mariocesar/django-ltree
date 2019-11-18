from django_ltree.fields import PathField
from django_ltree import lookups, functions


def test_registered_lookups():
    registered_lookups = PathField.get_lookups()

    assert "ancestors" in registered_lookups, "Missing 'ancestors' in lookups"
    assert registered_lookups["ancestors"] is lookups.AncestorLookup

    assert "descendants" in registered_lookups, "Missing 'descendants' in lookups"
    assert registered_lookups["descendants"] is lookups.DescendantLookup

    assert "match" in registered_lookups, "Missing 'match' in lookups"
    assert registered_lookups["match"] is lookups.MatchLookup

    assert "depth" in registered_lookups, "Missing 'depth' in lookups"
    assert registered_lookups["depth"] is functions.NLevel

    assert "contains" in registered_lookups, "Missing 'contains' in lookups"
    assert registered_lookups["contains"] is lookups.ContainsLookup

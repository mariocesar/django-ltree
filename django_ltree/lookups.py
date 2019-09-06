from django.db.models import IntegerField, Lookup, Transform

from .fields import PathField


class SimpleLookup(Lookup):
    lookup_operator = "="  # type: str

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return "{} {} {}".format(lhs, self.lookup_operator, rhs), params


@PathField.register_lookup
class EqualLookup(Lookup):
    lookup_name = "exact"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params

        return "{} = {}".format(lhs, rhs), params


@PathField.register_lookup
class AncestorLookup(SimpleLookup):
    lookup_name = "ancestors"
    lookup_operator = "@>"


@PathField.register_lookup
class DescendantLookup(SimpleLookup):
    lookup_name = "descendants"
    lookup_operator = "<@"


@PathField.register_lookup
class MatchLookup(SimpleLookup):
    lookup_name = "match"
    lookup_operator = "~"

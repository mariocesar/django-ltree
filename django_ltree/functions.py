from django.db.models import Value, fields
from django.db.models.expressions import Func

from .fields import PathField


class NLevel(Func):
    function = "NLEVEL"
    output_field = fields.IntegerField()
    arity = 1

    def __init__(self, expression, **extra):
        super().__init__(expression, **extra)


class Subpath(Func):
    function = "SUBPATH"
    output_field = PathField()

    def __init__(self, *expressions, output_field=None, **extra):
        if len(expressions) != 2 and len(expressions) != 3:
            raise ValueError("Subpath takes either 2 or 3 arguments")
        super().__init__(*expressions, output_field=output_field, **extra)


__all__ = ("NLevel", "Subpath")

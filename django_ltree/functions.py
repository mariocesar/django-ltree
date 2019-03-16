from django.db.models import Transform
from django.db.models import fields

__all__ = ("NLevel",)


class NLevel(Transform):
    lookup_name = "depth"
    function = "nlevel"
    output_field = fields.IntegerField()

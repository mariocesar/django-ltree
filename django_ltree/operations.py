from django.contrib.postgres.operations import CreateExtension


class LtreeExtension(CreateExtension):
    def __init__(self, name=None, **kwargs):
        super().__init__("ltree", **kwargs)

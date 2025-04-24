from django.contrib.postgres.operations import CreateExtension


class LtreeExtension(CreateExtension):
    def __init__(self):
        self.name = "ltree"

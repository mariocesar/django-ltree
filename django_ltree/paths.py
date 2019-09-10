from itertools import product

from django_ltree.fields import PathValue


class PathGenerator(object):

    _alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _label_size = 8  # Postgres limits this to 256

    def __init__(self, prefix=None, skip=None):
        self.skip_paths = [] if skip is None else skip[:]
        self.path_prefix = prefix if prefix else []
        self.product_iterator = product(self._alphabet, repeat=self._label_size)

    def __iter__(self):
        return self

    def __next__(self):
        label = ''.join(self.product_iterator.next())
        path = PathValue(self.path_prefix + [label])
        while path in self.skip_paths:
            label = ''.join(self.product_iterator.next())
            path = PathValue(self.path_prefix + [label])
        return path

    next = __next__
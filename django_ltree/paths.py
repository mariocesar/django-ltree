from itertools import product

from django_ltree.fields import PathValue


class PathGenerator(object):

    _alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _default_label_size = 6  # Postgres limits this to 256

    def __init__(self, prefix=None, skip=None, label_size=None):
        self.skip_paths = [] if skip is None else skip[:]
        self.path_prefix = prefix if prefix else []
        self.product_iterator = product(self._alphabet, repeat=label_size or self._default_label_size)

    def __iter__(self):
        return self

    def __next__(self):
        for val in self.product_iterator:
            label = ''.join(val)
            path = PathValue(self.path_prefix + [label])
            if path not in self.skip_paths:
                return path

    next = __next__

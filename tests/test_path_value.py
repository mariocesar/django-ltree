import pytest

from django_ltree.fields import PathValue


def test_create():
    assert str(PathValue([1, 2, 3, 4, 5])) == '1.2.3.4.5'
    assert str(PathValue((1, 3, 5, 7))) == '1.3.5.7'
    assert str(PathValue('hello.world')) == 'hello.world'
    assert str(PathValue(5)) == "5"

    def generator():
        yield '100'
        yield 'bottles'
        yield 'of'
        yield 'beer'

    assert str(PathValue(generator())) == '100.bottles.of.beer'

import pytest

from uniontypes import union


# doctest the generated docstring for uniontypes
__test__ = {'test_docstring': union(list, tuple, str)}


def test_not_enough_args():
    with pytest.raises(TypeError):
        union()

    with pytest.raises(TypeError):
        union(type)


def test_union_str():
    assert str(union(list, str)('test')) == 'Union[list, str][str] test'
    assert str(union(list, str)([1, 2])) == 'Union[list, str][list] [1, 2]'

import pytest

from uniontypes import Union


# doctest the generated docstring for uniontypes
__test__ = {'test_docstring': Union[list, tuple, str]}


def test_create_union_instance():
    with pytest.raises(TypeError):
        Union()


def test_not_enough_args():
    with pytest.raises(TypeError):
        Union[type]


def test_union_str():
    assert str(Union[list, str]('test')) == 'Union[list, str][str] test'
    assert str(Union[list, str]([1, 2])) == 'Union[list, str][list] [1, 2]'

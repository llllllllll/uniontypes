from uniontypes import Option


def test_option_name():
    assert Option[int].__name__ == 'Option[int]'


def test_nothing():
    oint = Option[int]
    nothing = oint(None)
    assert nothing is oint(None) is oint.nothing
    assert str(nothing) == 'Nothing'

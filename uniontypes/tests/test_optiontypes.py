from uniontypes import option


def test_option_name():
    assert option(int).__name__ == 'Option[int]'


def test_nothing():
    oint = option(int)
    nothing = oint(None)
    assert nothing is oint(None) is oint.nothing
    assert str(nothing) == 'Nothing'

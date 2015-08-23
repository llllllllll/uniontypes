from metautils.box import box
from multipledispatch import dispatch
from toolz import memoize, curry


@memoize
def union(*types, _isoption=False):
    """Construct a disjoint-union type out of some types.

    Paramaters
    ----------
    *types : iterable of type
        The types to wrap.

    Returns
    -------
    Union : type
        A type that is a union type of all the arguments.

    See Also
    --------
    uniontype.option
    """
    if len(types) < 2:
        raise TypeError('union needs at least 2 types')

    class Union(metaclass=UnionMeta):
        """A union type.
        """
        def __str__(self):
            return '%s %s' % (type(self).__name__, self.unboxed)

        def __repr__(self):
            return '%s %r' % (type(self).__name__, self.unboxed)

    type_names = [getattr(type_, '__name__', str(type_)) for type_ in types]
    Union.__doc__ = _union_docfmt.format(
        newline_types='\n    '.join(type_names),
        or_=' or '.join(type_names),
    )
    if _isoption:
        type_ = types[0]
        Union.__name__ = Union.__qualname__ = (
            'Option[%s]' % getattr(type_, '__name__', type_)
        )
    else:
        Union.__name__ = Union.__qualname__ = (
            'Union[%s]' % ', '.join(type_names)
        )

    dispatch_ns = {}
    Union._types = typemap = {}

    mkwrapper = _mkoption_wrapper if _isoption else _mkwrapper
    for type_, wrapper in map(mkwrapper(Union), types):
        typemap[type_] = wrapper

        def bind(wrapper=wrapper):
            """Closure for early binding
            """
            @dispatch(type, type_, namespace=dispatch_ns)
            def __new__(cls, value):
                return wrapper(value)
            return __new__

        __new__ = bind()
    Union.__new__ = __new__
    return Union


def option(type_):
    """Construct an option type over another type.

    Paramaters
    ----------
    type_ : type
        The types to use as the non-none type.

    Returns
    -------
    Option : type
        A type that can hold either instances of ``type_`` or None.

    See Also
    --------
    uniontypes.union
    """
    nonetype = type(None)
    u = union(type_, nonetype, _isoption=True)
    u._types[None] = u[nonetype]
    u.nothing = u(None)
    return u


_union_docfmt = """A union type of:

    {newline_types}

Users may index this type with one of the subtypes to get the wrapper for
that type.

Paramaters
----------
value : {or_}
    The value to box.

Attributes
----------
unboxed : {or_}
    The unboxed value.


Examples
--------
Creating a union type
>>> u = union(list, tuple, str)
>>> u
<class 'uniontypes.Union[list, tuple, str]'>

Creating boxed values
>>> u([1, 2, 3])
Union[list, tuple, str][list] [1, 2, 3]
>>> u((1, 2, 3))
Union[list, tuple, str][tuple] (1, 2, 3)
>>> u('123')
Union[list, tuple, str][str] '123'

Accessing the inner wrapper types
>>> u[list]
<class 'uniontypes.Union[list, tuple, str][list]'>
>>> u[tuple]
<class 'uniontypes.Union[list, tuple, str][tuple]'>
>>> u[str]
<class 'uniontypes.Union[list, tuple, str][str]'>

Class heirarchy
>>> isinstance(u([1, 2, 3]), u)
True
>>> isinstance(u([1, 2, 3]), u[list])
True
>>> isinstance(u([1, 2, 3]), (u[tuple], u[str]))
False

See Also
--------
uniontypes.union
uniontypes.option
"""


class UnionMeta(type):
    def __getitem__(self, type_):
        return self._types[type_]


@curry
def _mkwrapper(parent, type_):
    class Wrapper(box, parent):
        __new__ = object.__new__

    Wrapper.__name__ = Wrapper.__qualname__ = '%s[%s]' % (
        parent.__name__, getattr(type_, '__name__', str(type_)),
    )

    return type_, Wrapper


@curry
def _mkoption_wrapper(parent, type_):
    if issubclass(type_, type(None)):
        nothing_instance = None

        class Wrapper(box, parent):
            def __new__(cls, value):
                nonlocal nothing_instance
                if nothing_instance is None:
                    nothing_instance = object.__new__(cls)
                return nothing_instance

            def __str__(self):
                return 'Nothing'
            __repr__ = __str__

        name = 'Nothing'
    else:
        class Wrapper(box, parent):
            __new__ = object.__new__

        name = parent.__name__

    Wrapper.__name__ = Wrapper.__qualname__ = name
    return type_, Wrapper

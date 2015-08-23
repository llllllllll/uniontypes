``uniontypes 0.1``
============

|build status|

Union types For python.

These appear other languages like Haskell (``Either``) and
Scala (``Union`` or ``\/``).

This extends to any arbirary set of types.


Examples
--------
Creating a union type
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   >>> u = union(list, tuple, str)
   >>> u
   <class 'uniontypes.Union[list, tuple, str]'>

Creating boxed values
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   >>> u([1, 2, 3])
   Union[list, tuple, str][list] [1, 2, 3]
   >>> u((1, 2, 3))
   Union[list, tuple, str][tuple] (1, 2, 3)
   >>> u('123')
   Union[list, tuple, str][str] '123'

Accessing the inner wrapper types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   >>> u[list]
   <class 'uniontypes.Union[list, tuple, str][list]'>
   >>> u[tuple]
   <class 'uniontypes.Union[list, tuple, str][tuple]'>
   >>> u[str]
   <class 'uniontypes.Union[list, tuple, str][str]'>

Class heirarchy
~~~~~~~~~~~~~~~
.. code-block:: python

   >>> isinstance(u([1, 2, 3]), u)
   True
   >>> isinstance(u([1, 2, 3]), u[list])
   True
   >>> isinstance(u([1, 2, 3]), (u[tuple], u[str]))
   False

Option Types
------------
.. code-block:: python

   >>> oint = option(int)
   >>> oint
   <class 'uniontypes.Option[int]'>
   >>> oint(1)
   Option[int] 1
   >>> oint(None)
   Nothing
   >>> oint(None) is oint.nothing
   True


.. |build status| image:: https://travis-ci.org/llllllllll/uniontypes.svg?branch=master
   :target: https://travis-ci.org/llllllllll/uniontypes

"""
.. _usr03:

Configuring datatypes
=====================

One of the translation challenges is how each variable type determined. In C++
all variables have to be explicitly declared, while in Matlab they are declared
implicitly at creation.  When translating between the two languages, there are
many variables where the data types are unknown and impossible for the
Matlab2cpp software to translate.  How to translate the behavior of an integer
is vastly different from an float matrix.

As noted in the last section :ref:`usr02`, each node can have multiple
backends. At the simplest level, each node have
a :py:mod:`~matlab2cpp.datatype` which represents what backend rule should be
used in translation. 

Datatypes can be roughly split into two groups: **numerical** and
**non-numerical** types.  The numerical types are as follows:

+-----------------+--------------+---------+---------+--------+-----------+
|                 | unsigned int | int     | float   | double | complex   |
+=================+==============+=========+=========+========+===========+
| **scalar**      | uword        | int     | float   | double | cx_double |
+-----------------+--------------+---------+---------+--------+-----------+
| **vector**      | uvec         | ivec    | fvec    | vec    | cx_vec    |
+-----------------+--------------+---------+---------+--------+-----------+
| **row\-vector** | urowvec      | irowvec | frowvec | rowvec | cx_rowvec |
+-----------------+--------------+---------+---------+--------+-----------+
| **matrix**      | umat         | imat    | fmat    | mat    | cx_mat    |
+-----------------+--------------+---------+---------+--------+-----------+
| **cube**        | ucube        | icube   | fcube   | cube   | cx_cube   |
+-----------------+--------------+---------+---------+--------+-----------+

Values along the horizontal axis represents the amount of memory reserved per
element, and the along the vertical axis represents the various number of
dimensions.  The names are equivalent to the ones in the Armadillo package.

The non-numerical types are as follows:

+-----------------+------------------------+
| Name            | Description            |
+=================+========================+
| **char**        | Single text character  |
+-----------------+------------------------+
| **string**      | Text string            |
+-----------------+------------------------+
| **struct**      | Struct container       |
+-----------------+------------------------+
| **structs**     | Struct array container |
+-----------------+------------------------+
| **func_lambda** | Anonymous function     |
+-----------------+------------------------+

The node datatype can be referenced by any node through `node.type` and can be
inserted as placeholder through `%(type)s`. For example::

    >>> def Var(node):
    ...     if node.name == "x":    node.type = "vec"
    ...     else:                   node.type = "rowvec"
    ...     return node.name
    >>> print mc.qscript("function f(x,y)", Var=Var)
    void f(vec x, rowvec y)
    {
      // Empty block
    }

Function scope
--------------

If not specified otherwise, the program will not assign datatype types to any
of variables. The user could in theory navigate the node tree and assign the
variables one by one using the node attributes to navigate. (See :ref:`usr04`
for details.) However that would be very cumbersome. Instead the datatypes are
define collectively inside their scope. In the case of variables in functions,
the scope variables are the variables declaration
:py:class:`~matlab2cpp.Declares` and function parameters
:py:class:`~matlab2cpp.Params`. To reach the variable that serves as
a scope-wide type, the node attribute :py:attr:`~matlab2cpp.Node.declare` can
be used.

Manually interacting with the variable scope is simpler then iterating through
the full tree, but can in many cases still be

can
be inserted much simpler into the program using supplement attribute 
:py:attr:`~matlab2cpp.Node.ftypes`. The attribute is a nested dictionary where
the outer shell represents the function name the variables are defined. The
inner shell is the variables where keys are variable names and values are
types. For example::

    >>> tree = mc.build("function f(a)")
    >>> print tree.ftypes
    {'f': {'a': ''}}
    >>> tree.ftypes = {"f": {"a": "int"}}
    >>> print mc.qscript(tree)
    void f(int a)
    {
      // Empty block
    }

Here there is one function scope defined by `f`, with one variable `a`.




Anonymous functions
~~~~~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.functions

Data structures
~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.structs

Suggestions
~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.suggests

Includes
~~~~~~~~
.. automodule:: matlab2cpp.supplement.includes

Suggestion engine
-----------------
.. automodule:: matlab2cpp.configure
"""
import matlab2cpp as mc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
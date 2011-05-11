#!/usr/bin/env python

"""
Design
"""

from types import FunctionType, MethodType
from inspect import getsource

from couchdb.design import ViewDefinition
from couchdb.design import _strip_decorators


class EnhancedViewDefinition(ViewDefinition):
    """
    Modified View Definition Decorator
    """

    def __init__(self,
                 design,
                 name,
                 map_fun,
                 reduce_fun=None,
                 language='javascript',
                 wrapper=None,
                 **defaults):
        """
        Initialize the view definition.

        Note that the code in `map_fun` and `reduce_fun` is automatically
        dedented, that is, any common leading whitespace is removed from each
        line.

        :param design: the name of the design document
        :param name: the name of the view
        :param map_fun: the map function code
        :param reduce_fun: the reduce function code (optional)
        :param language: the name of the language used
        :param wrapper: an optional callable that should be used to wrap the
                        result rows
        """
        if isinstance(reduce_fun, FunctionType) or \
                isinstance(reduce_fun, MethodType):
            reduce_fun = _strip_decorators(getsource(reduce_fun).rstrip())
        super(EnhancedViewDefinition,
              self).__init__(design,
                             name,
                             map_fun,
                             reduce_fun,
                             language,
                             wrapper,
                             **defaults)
        return None

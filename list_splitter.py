#!/usr/bin/env python

"""
Goodies for helping with iterables
"""

import math
from itertools import izip
from collections import Iterable


def chunks_matrix(r, chunk_size, width):
    """
    Builds a chunk matrix
    """
    return chunks_of_n(chunks_of_n(r, chunk_size), width)


def n_chunks(r, n):
    """
    Splits an iterable in n chunks.
    Accepts dicts, lists, tuples, and
    some types of generators
    """
    s = int(math.ceil(float(len(r)) / float(n)))
    return _chunks(r, s)


def chunks_of_n(r, n):
    """
    Alias for `_chunks`
    """
    return _chunks(r, n)


def _chunks(r, n):
    """
    Splits an iterable into chunks of n.
    Accepts dicts, lists, tuples, and some types
    of generators.
    """
    ##
    ## Dict
    ##
    if isinstance(r, dict):
        if len(r) == 0:
            out = iter([])
        else:
            keys, vals = izip(*r.iteritems())
            out = (
                dict((keys[ii], vals[ii]) for ii in xrange(i, i + n)
                     if ii < len(r))
                for i in xrange(0, len(r), n)
            )
    ##
    ## List or anything that has a length and is sliceable.
    ## This most likely includes a Django QuerySet result
    ##
    elif isinstance(r, Iterable) and \
            hasattr(r, '__len__') and \
            hasattr(r, '__getitem__'):
        out = (r[i:i + n] for i in xrange(0, len(r), n))
    ##
    ## Some other generator that can be converted
    ## to a list
    ##
    elif isinstance(r, Iterable):
        ri = list(r)
        out = (ri[i:i + n] for i in xrange(0, len(ri), n))
    ##
    ## Unknown
    ##
    else:
        raise Exception('Cannot chunkify!!')
    return out

"""
utils for file validator
"""
from itertools import groupby


def all_mimes_is_equal(iterable):
    """Returns True if all the elements are equal to each other"""
    group = groupby(iterable)
    return next(group, True) and not next(group, False)

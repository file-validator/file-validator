"""
utils for file validator
"""
from itertools import groupby

from termcolor import colored

from file_validator.constants import ALL_SUPPORTED_LIBRARIES, LIBRARY_IS_NOT_SUPPORTED
from file_validator.exceptions import LibraryNotSupportedException


def all_mimes_is_equal(mimes):
    """
    Returns True if all the mimes are equal to each other
    if the length of mimes is one returned false
    """
    if len(mimes) == 1:
        return False
    group = groupby(mimes)
    return next(group, True) and not next(group, False)


def is_library_supported(library: str):
    """
    If we do not support the library you choose, a LibraryNotSupporteexception error is thrown.
    supported libraries: python magic, pure magic, filetype, mimetypes
    """
    if library not in ALL_SUPPORTED_LIBRARIES:
        message = LIBRARY_IS_NOT_SUPPORTED.format(
            library=library, libraries=ALL_SUPPORTED_LIBRARIES
        )
        raise LibraryNotSupportedException(colored(message, "red"))

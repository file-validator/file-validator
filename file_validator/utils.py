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


def generate_information_about_file(
    status=None, library=None, file_name=None, file_extension=None, file_mime=None, **kwargs
) -> dict:
    """
    generates information about file validated
    """
    result = {}
    file_type = kwargs.get("file_type")
    if status is not None:
        result.update({"status": status})
    if library is not None:
        result.update({"library": library})
    if file_name is not None:
        result.update({"file_name": file_name})
    if file_type is not None:
        result.update({"file_type": file_type})
    if file_mime is not None:
        result.update({"file_mime": file_mime})
    if file_extension is not None:
        result.update({"file_extension": file_extension})

    return result

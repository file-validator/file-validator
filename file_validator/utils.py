"""utils for file validator."""
from itertools import groupby

from filetype import is_archive, is_audio, is_font, is_image, is_video
from termcolor import colored

from file_validator.constants import (
    ALL_SUPPORTED_LIBRARIES,
    ARCHIVE,
    AUDIO,
    FONT,
    IMAGE,
    LIBRARY_IS_NOT_SUPPORTED,
    MIMES_IS_EQUAL,
    PARAMETERS_ARE_EMPTY,
    VIDEO,
)
from file_validator.exceptions import (
    EmptyParametersException,
    LibraryNotSupportedException,
    MimesEqualException,
)


def all_mimes_is_equal(acceptable_mimes):
    """Returns True if all the mimes are equal to each other if the length of
    mimes is one returned false."""
    if acceptable_mimes is not None:
        if len(acceptable_mimes) == 1:
            mimes_is_equal = False
        group = groupby(acceptable_mimes)
        mimes_is_equal = next(group, True) and not next(group, False)
        if mimes_is_equal:
            raise MimesEqualException(colored(MIMES_IS_EQUAL, "red"))


def is_library_supported(library: str):
    """If we do not support the library you choose, a
    LibraryNotSupporteexception error is thrown.

    supported libraries: python magic, pure magic, filetype, mimetypes
    """
    if library not in ALL_SUPPORTED_LIBRARIES:
        message = LIBRARY_IS_NOT_SUPPORTED.format(
            library=library,
            libraries=ALL_SUPPORTED_LIBRARIES,
        )
        raise LibraryNotSupportedException(colored(message, "red"))


def generate_information_about_file(
    status=None,
    library=None,
    file_name=None,
    file_extension=None,
    file_mime=None,
    **kwargs
) -> dict:
    """generates information about file validated."""
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


def guess_the_type(file_path: str):
    """This function is used to guess the overall type of file such image,
    audio, video, font and archive."""
    if is_video(file_path):
        return VIDEO
    if is_image(file_path):
        return IMAGE
    if is_audio(file_path):
        return AUDIO
    if is_font(file_path):
        return FONT
    if is_archive(file_path):
        return ARCHIVE
    return None


def parameters_are_empty(acceptable_types, acceptable_mimes):
    """this function check whether parameters are empty or no ?"""
    if acceptable_types is None and acceptable_mimes is None:
        raise EmptyParametersException(colored(PARAMETERS_ARE_EMPTY, "red"))

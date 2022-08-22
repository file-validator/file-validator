"""
In this module, there is a file validator for python,
and it uses different libraries such as filetype,
python-magic, mimetypes, and files are validated based
on mimes, extensions, and magic numbers; The termcolor
library is also used to color the error messages
"""

from mimetypes import guess_type
import magic
import puremagic
from filetype import guess
from termcolor import colored

from .constants import MIME_NOT_VALID, MIME_NOT_VALID_WITH_MIME_NAME


def file_validator_by_python_magic(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        with open(file_path, "rb") as file:
            file_mime = magic.from_buffer(file.read(2048), mime=True)
    except AttributeError as error:
        raise ValueError(colored(MIME_NOT_VALID, "red")) from error

    if file_mime not in mimes:
        raise ValueError(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_mimetypes(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        file_mime = guess_type(file_path)[0]
    except AttributeError as error:
        raise ValueError(colored(MIME_NOT_VALID, "red")) from error
    if file_mime not in mimes:
        raise ValueError(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_filetype(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        file_mime = guess(file_path).MIME
    except AttributeError as error:
        raise ValueError(colored(MIME_NOT_VALID, "red")) from error

    if file_mime not in mimes:
        raise ValueError(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_pure_magic(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        with open(file_path, "rb") as file:
            file_signatures = puremagic.magic_stream(file)
            file_mimes = []
            for file_signature in file_signatures:
                file_mimes.append(file_signature.mime_type)
    except AttributeError as error:
        raise ValueError(colored(MIME_NOT_VALID, "red")) from error

    mimes_is_equal = len(set(file_mimes)) <= 1
    if mimes_is_equal:
        file_mime = file_mimes[0]
        if file_mime not in mimes:
            raise ValueError(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red"
                )
            )


def file_validator(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        file_validator_by_filetype(mimes, file_path)
        file_validator_by_mimetypes(mimes, file_path)
        file_validator_by_pure_magic(mimes, file_path)
        file_validator_by_python_magic(mimes, file_path)
    except AttributeError as error:
        raise ValueError(colored(MIME_NOT_VALID, "red")) from error

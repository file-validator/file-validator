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


def file_validator_by_python_magic(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    with open(file_path, "rb") as file:
        file_mime = magic.from_buffer(file.read(2048), mime=True)
    if file_mime not in mimes:
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator_by_mimetypes(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess_type(file_path)[0]
    if file_mime not in mimes:
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator_by_filetype(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess(file_path).MIME
    if file_mime not in mimes:
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator_by_pure_magic(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    with open(file_path, "rb") as file:
        file_signatures = puremagic.magic_stream(file)
        file_mimes = []
        for file_signature in file_signatures:
            file_mimes.append(file_signature.mime_type)
    mimes_is_equal = len(set(file_mimes)) <= 1
    if mimes_is_equal:
        file_mime = file_mimes[0]
        if file_mime not in mimes:
            error_message = f"{file_mime} is not valid"
            raise ValueError(colored(error_message, "red"))


def file_validator(mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type mimes: list
    :param mimes: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_validator_by_filetype(mimes, file_path)
    file_validator_by_mimetypes(mimes, file_path)
    file_validator_by_pure_magic(mimes, file_path)
    file_validator_by_python_magic(mimes, file_path)

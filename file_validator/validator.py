"""
In this module, there is a file validator for python,
and it uses different libraries such as filetype,
python-magic, mimetypes, and files are validated based
on mimes, extensions, and magic numbers; The termcolor
library is also used to color the error messages
"""

from mimetypes import guess_type
import magic
from filetype import guess
from termcolor import colored


def file_validator_by_python_magic(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    with open(file_path, "rb") as file:
        file_mime = magic.from_buffer(file.read(2048), mime=True)
    if file_mime not in list(args):
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator_by_mimetypes(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess_type(file_path)[0]
    if file_mime not in list(args):
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator_by_filetype(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess(file_path).MIME
    if file_mime not in list(args):
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.

    """
    file_validator_by_filetype(*args, file_path=file_path)
    file_validator_by_mimetypes(*args, file_path=file_path)
    file_validator_by_python_magic(*args, file_path=file_path)

"""
In this module, there is a file validator for python,
and it uses different libraries such as filetype,
python-magic, mimetypes, and files are validated based
on mimes, extensions, and magic numbers; The termcolor
library is also used to color the error messages
"""

from mimetypes import guess_type
import os
import platform
import magic
import puremagic
from filetype import guess
from humanize import naturalsize
from puremagic import PureError
from termcolor import colored
from dotenv import load_dotenv

from file_validator.exceptions import (
    error_message,
    FileValidationException,
    SizeValidationException,
)
from file_validator.constants import (
    PYTHON_MAGIC,
    PURE_MAGIC,
    FILETYPE,
    MIME_NOT_VALID,
    MIMETYPES,
    FILE_SIZE_IS_NOT_VALID,
    MIME_NOT_VALID_WITH_MIME_NAME,
    ALL,
)
from file_validator.utils import is_library_supported


def file_validator_by_python_magic(acceptable_mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type acceptable_mimes: list
    :param acceptable_mimes: The mime of the files you want to validate based on them,
        example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    load_dotenv()
    operating_system_name = platform.system()
    path_magic_file = os.environ.get("path_magic_file")
    if path_magic_file and operating_system_name == 'Windows':
        with open(file_path, "rb") as file:
            magic.Magic(magic_file=path_magic_file)
            file_mime = magic.from_buffer(file.read(2048), mime=True)
    else:
        with open(file_path, "rb") as file:
            file_mime = magic.from_buffer(file.read(2048), mime=True)

    if file_mime not in acceptable_mimes:
        raise FileValidationException(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_pure_magic(acceptable_mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type acceptable_mimes: list
    :param acceptable_mimes: The mime of the files you want to validate based on them,
        example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        with open(file_path, "rb") as file:
            file_signatures = puremagic.magic_stream(file)
            file_mimes = []
            for file_signature in file_signatures:
                file_mimes.append(file_signature.mime_type)
    except PureError as error:
        raise FileValidationException(colored(MIME_NOT_VALID, "red")) from error

    file_mime = file_mimes[0]
    if file_mime not in acceptable_mimes:
        raise FileValidationException(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_mimetypes(acceptable_mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type acceptable_mimes: list
    :param acceptable_mimes: The mime of the files you want to validate based on them,
        example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess_type(file_path)[0]
    if file_mime is None:
        raise FileValidationException(colored(MIME_NOT_VALID, "red"))

    if file_mime not in acceptable_mimes:
        raise FileValidationException(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator_by_filetype(acceptable_mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type acceptable_mimes: list
    :param acceptable_mimes: The mime of the files you want to validate based on them,
        example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """
    try:
        file_mime = guess(file_path).MIME
    except AttributeError as error:
        raise FileValidationException(colored(MIME_NOT_VALID, "red")) from error

    if file_mime not in acceptable_mimes:
        raise FileValidationException(
            colored(MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime), "red")
        )


def file_validator(acceptable_mimes: list, file_path: str):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :type acceptable_mimes: list
    :param acceptable_mimes: The mime of the files you want to validate based on them,
        example: image/png
    :return: If everything is OK it will return None, otherwise it will return a ValueError.
    """

    file_validator_by_filetype(acceptable_mimes, file_path)
    file_validator_by_mimetypes(acceptable_mimes, file_path)
    file_validator_by_pure_magic(acceptable_mimes, file_path)
    file_validator_by_python_magic(acceptable_mimes, file_path)


def size_validator(
    file_path: str,
    max_upload_file_size: int,
):
    """
    :type max_upload_file_size: int
    :param max_upload_file_size: The most size file that the user is able to upload
    :type file_path: str
    :param file_path: The file path to be validated
    :return: If everything is OK it will return None, otherwise it will
        return a SizeValidationException.
    """
    file_size = os.path.getsize(file_path)
    if max_upload_file_size is not None and file_size > max_upload_file_size:
        raise SizeValidationException(
            error_message(
                file_size=naturalsize(file_size),
                max_file_size=naturalsize(max_upload_file_size),
                message=FILE_SIZE_IS_NOT_VALID,
            )
        )


def file_validator_by_django(
    content_type_guessed_by_django: str,
    acceptable_mimes: list,
    file_path: str,
    libraries: list,
):
    """
    :type libraries: list
    :param libraries:The value of libraries should be a list of libraries with which you
        want to perform the validation operation, example: libraries=["filetype","python_magic"]
        defaults If you do not select any library, it will perform the validation operation with
        all libraries by default, Supported libraries for validation operations: python_magic,
        pure_magic, filetype, mimetypes
    :type acceptable_mimes: list
    :param acceptable_mimes: The mimes you want the file to be checked based on, example: image/png
    :type file_path: string
    :param file_path: The file path to be validated
    :type content_type_guessed_by_django: Mime that guessed by Django
    :param content_type_guessed_by_django: string
    :return: If everything is OK it will return None, otherwise it will
        return a FileValidationException.
    """
    for library in libraries:
        is_library_supported(library)

        if library == ALL:
            file_validator(acceptable_mimes=acceptable_mimes, file_path=file_path)

        elif library == PYTHON_MAGIC:
            file_validator_by_python_magic(acceptable_mimes=acceptable_mimes, file_path=file_path)

        elif library == PURE_MAGIC:
            file_validator_by_pure_magic(acceptable_mimes=acceptable_mimes, file_path=file_path)

        elif library == FILETYPE:
            file_validator_by_filetype(acceptable_mimes=acceptable_mimes, file_path=file_path)

        elif library == MIMETYPES:
            file_validator_by_mimetypes(acceptable_mimes=acceptable_mimes, file_path=file_path)

        else:
            if content_type_guessed_by_django not in acceptable_mimes:
                raise FileValidationException(
                    colored(
                        MIME_NOT_VALID_WITH_MIME_NAME.format(
                            file_mime=content_type_guessed_by_django
                        ),
                        "red",
                    )
                )

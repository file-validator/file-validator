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

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

from .exceptions import error_message
from .constants import (
    ZERO,
    SELECTING_ALL_SUPPORTED_LIBRARIES,
    PYTHON_MAGIC,
    MIMES_EMPTY,
    PURE_MAGIC,
    FILETYPE,
    MIME_NOT_VALID,
    MIMETYPES, DEFAULT,
    FILE_SIZE_IS_NOT_VALID,
    MIME_NOT_VALID_WITH_MIME_NAME, ALL_SUPPORTED_LIBRARIES, LIBRARY_IS_NOT_SUPPORTED
)


@deconstructible
class FileValidator:
    """
    In this module, there are file validators for Django,
    and it is made using external libraries such as (filetype, python-magic)
    and native libraries such as (mimetypes), and there is a method to perform
    validation operations using all three libraries It is called safe mode
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(
        self,
        libraries: list = None,
        acceptable_mimes: list = None,
        max_upload_file_size: int = 0,
    ):
        """
        :type acceptable_mimes: list
        :param acceptable_mimes: The mimes you want the file to be checked
            based on, example: image/png
        :type max_upload_file_size: int, optional
        :param max_upload_file_size: If you want the file size to be checked,
            the file size must be in bytes,
            example: file_size=1048576 (1MB), defaults to 0, optional
        :type libraries: list, optional
        :param libraries: The value of libraries should be a list of libraries
            with which you want to perform the validation operation, example:
            libraries=["filetype","python_magic"] defaults If you do not select
            any library, it will perform the validation operation with all
            libraries by default, Supported libraries for validation operations:
            python_magic, pure_magic, filetype, mimetypes
        :raises ValueError: If the mime list is empty, raised a value error
        :raises ValueError: If the library you entered is not supported,
            raised a value error, Supported library: filetype, mimetypes,
            pure_magic, python_magic
        """
        if max_upload_file_size != ZERO:
            self.max_upload_file_size = max_upload_file_size
        else:
            self.max_upload_file_size = ZERO

        self.libraries = []
        if libraries is None:
            self.libraries.append(SELECTING_ALL_SUPPORTED_LIBRARIES)
        else:
            for library in libraries:
                if library not in ALL_SUPPORTED_LIBRARIES:
                    message = LIBRARY_IS_NOT_SUPPORTED.format(
                        library=library, libraries=ALL_SUPPORTED_LIBRARIES
                    )
                    raise ValueError(colored(message, "red"))
                self.libraries.append(library)

        if acceptable_mimes is None or not all(acceptable_mimes):
            raise ValueError(colored(MIMES_EMPTY, "red"))

        self.acceptable_mimes = []
        for mime in acceptable_mimes:
            self.acceptable_mimes.append(mime)

    def __call__(self, value):
        file = value.file
        file_size = file.size
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        content_type_guessed_by_django = file.content_type
        size_validator(
            max_upload_file_size=self.max_upload_file_size,
            acceptable_mimes=self.acceptable_mimes,
            file_size=file_size,
            file=file
        )
        try:
            file_validator_by_django(
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                file_path=file_path,
                content_type_guessed_by_django=content_type_guessed_by_django
            )
        except ValueError as error:
            raise ValidationError(
                error_message(
                    file=file,
                    file_size=filesizeformat(file_size),
                    max_file_size=filesizeformat(self.max_upload_file_size),
                    mimes=self.acceptable_mimes,
                )
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.libraries == other.libraries
            and self.acceptable_mimes == other.acceptable_mimes
            and self.max_upload_file_size == other.max_upload_file_size
        )


def file_validator_by_python_magic(
    mimes: list, file_path: str
):
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


def file_validator_by_pure_magic(
    mimes: list,
    file_path: str
):
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


def file_validator_by_mimetypes(
    mimes: list,
    file_path: str
):
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


def file_validator_by_filetype(
    mimes: list,
    file_path: str
):
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


def file_validator_by_django(
    content_type_guessed_by_django: str,
    acceptable_mimes: list,
    libraries: list,
    file_path: str
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
    :param file_path:
    :type content_type_guessed_by_django:
    :param content_type_guessed_by_django: string
    :return:yyy
    """
    for library in libraries:
        if library not in ALL_SUPPORTED_LIBRARIES:
            message = LIBRARY_IS_NOT_SUPPORTED.format(
                library=library, libraries=ALL_SUPPORTED_LIBRARIES
            )
            raise ValueError(colored(message, "red"))
        if library == SELECTING_ALL_SUPPORTED_LIBRARIES:
            file_validator(mimes=acceptable_mimes, file_path=file_path)

        elif library == PYTHON_MAGIC:
            file_validator_by_python_magic(
                mimes=acceptable_mimes, file_path=file_path
            )

        elif library == PURE_MAGIC:
            file_validator_by_pure_magic(
                mimes=acceptable_mimes, file_path=file_path
            )

        elif library == FILETYPE:
            file_validator_by_filetype(
                mimes=acceptable_mimes, file_path=file_path
            )

        elif library == MIMETYPES:
            file_validator_by_mimetypes(
                mimes=acceptable_mimes, file_path=file_path
            )

        elif library == DEFAULT or len(libraries) == 0:
            if content_type_guessed_by_django not in acceptable_mimes:
                raise ValueError(
                    colored(
                        MIME_NOT_VALID_WITH_MIME_NAME.format(
                            file_mime=content_type_guessed_by_django),
                        "red")
                )


def file_validator(
    mimes: list,
    file_path: str
):
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


def size_validator(
    max_upload_file_size: int,
    acceptable_mimes: list,
    file_size: int,
    file
):
    """
    :type max_upload_file_size: int
    :param max_upload_file_size: The most size file that the user is able to upload
    :type file_size: int
    :param file_size: The size of the current file that has been uploaded
    :param file: Uploaded file
    :type acceptable_mimes: list
    :param acceptable_mimes: The mimes you want the file to be checked based on, example: image/png
    """
    if max_upload_file_size != ZERO and file_size > max_upload_file_size:
        raise ValidationError(
            error_message(
                file=file,
                mimes=acceptable_mimes,
                file_size=filesizeformat(file_size),
                max_file_size=filesizeformat(max_upload_file_size),
                message=FILE_SIZE_IS_NOT_VALID,
            )
        )

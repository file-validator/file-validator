"""In this module, there is a file validator for python, and it uses different
libraries such as filetype, python-magic, mimetypes, and files are validated
based on mimes, extensions, and magic numbers; The termcolor library is also
used to color the error messages."""

import os
import platform
from mimetypes import guess_type
from pathlib import Path

import magic
import puremagic
from dotenv import load_dotenv
from filetype import guess
from humanize import naturalsize
from puremagic import PureError
from termcolor import colored

from file_validator.constants import (
    DJANGO,
    FILE_EXTENSION_NOT_VALID,
    FILE_SIZE_IS_NOT_VALID,
    FILETYPE,
    MIME_NOT_VALID,
    MIME_NOT_VALID_WITH_MIME_NAME,
    MIMETYPES,
    OK,
    PURE_MAGIC,
    PYTHON_MAGIC,
    SIZE,
    SUPPORTED_TYPES,
    TYPE_NOT_SUPPORTED,
)
from file_validator.exceptions import (
    error_message,
    FileValidationException,
    SizeValidationException,
    TypeNotSupportedException,
)
from file_validator.utils import generate_information_about_file, guess_the_type


class FileValidator:
    """File validator."""

    # pylint: disable=too-many-instance-attributes
    # Eight are reasonable in this case.
    def __init__(
        self,
        file_path: str = None,
        libraries: list = None,
        acceptable_mimes: list = None,
        max_upload_file_size: int = None,
        **kwargs
    ):
        self.file_mime_guessed_by_django = kwargs.get("file_mime_guessed_by_django")
        self.acceptable_extensions = kwargs.get("acceptable_extensions")
        self.result_of_validation = {}
        self.max_upload_file_size = max_upload_file_size
        self.acceptable_mimes = acceptable_mimes
        self.acceptable_types = kwargs.get("acceptable_types")
        self.file_path = file_path
        self.libraries = libraries

    def validate_extension(self):
        """Test."""
        current_file = Path(self.file_path)
        file_extension = current_file.suffix
        if file_extension not in self.acceptable_extensions:
            raise FileValidationException(
                colored(
                    FILE_EXTENSION_NOT_VALID.format(file_extension=file_extension),
                    "red",
                ),
            )
        result_of_validation = {
            "file_extension": file_extension,
        }
        self.result_of_validation.update({SIZE: result_of_validation})
        return result_of_validation

    def validate_size(self):
        """Return.e."""
        file_size = os.path.getsize(self.file_path)
        if (
            self.max_upload_file_size is not None
            and file_size > self.max_upload_file_size
        ):
            raise SizeValidationException(
                error_message(
                    file_size=naturalsize(file_size),
                    max_file_size=naturalsize(self.max_upload_file_size),
                    message=FILE_SIZE_IS_NOT_VALID,
                ),
            )
        result_of_validation = {
            "file_size": naturalsize(file_size),
            "max_upload_file_size": naturalsize(self.max_upload_file_size)
            if self.max_upload_file_size is not None
            else 0,
        }
        self.result_of_validation.update({SIZE: result_of_validation})
        return result_of_validation

    def validate_type(self):
        """Testttgtg."""
        for acceptable_type in self.acceptable_types:
            if acceptable_type.lower() not in SUPPORTED_TYPES:
                raise TypeNotSupportedException(colored(TYPE_NOT_SUPPORTED, "red"))
        file_type = guess_the_type(self.file_path)
        if file_type not in self.acceptable_types:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_type),
                    "red",
                ),
            )
        current_file = Path(self.file_path)
        result_of_validation = generate_information_about_file(
            status=OK,
            library=FILETYPE,
            file_name=current_file.name,
            file_type=file_type,
            file_extension=current_file.suffix,
        )
        return result_of_validation

    def validate_mime(self):
        """Test."""
        load_dotenv()
        operating_system_name = platform.system()
        path_magic_file = os.environ.get("path_magic_file")
        if path_magic_file and operating_system_name == "Windows":
            with open(self.file_path, "rb") as file:
                magic.Magic(magic_file=path_magic_file)
                guessed_mime_by_python_magic = magic.from_buffer(
                    file.read(2048),
                    mime=True,
                )
        else:
            with open(self.file_path, "rb") as file:
                guessed_mime_by_python_magic = magic.from_buffer(
                    file.read(2048),
                    mime=True,
                )

        with open(self.file_path, "rb") as file:
            file_signatures = puremagic.magic_stream(file)
            file_mimes_by_pure_magic = []
            for file_signature in file_signatures:
                file_mimes_by_pure_magic.append(file_signature.mime_type)
        guessed_mime_by_pure_magic = file_mimes_by_pure_magic[0]

        guessed_mime_by_mimetypes = guess_type(self.file_path)[0]
        guessed_mime_by_filetype = guess(self.file_path).MIME
        guessed_mimes = [
            guessed_mime_by_python_magic,
            guessed_mime_by_pure_magic,
            guessed_mime_by_mimetypes,
            guessed_mime_by_filetype,
        ]
        for file_mime in self.acceptable_mimes:
            if file_mime not in guessed_mimes:
                raise FileValidationException(
                    colored(
                        MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime),
                        "red",
                    ),
                )

    def validate(self):
        """Test."""
        validation_data = {}

        validation_data_filetype = self.filetype()
        validation_data.update({FILETYPE: validation_data_filetype})

        validation_data_mimetypes = self.mimetypes()
        validation_data.update({MIMETYPES: validation_data_mimetypes})

        validation_data_pure_magic = self.pure_magic()
        validation_data.update({PURE_MAGIC: validation_data_pure_magic})

        validation_data_python_magic = self.python_magic()
        validation_data.update({PYTHON_MAGIC: validation_data_python_magic})

        if self.file_mime_guessed_by_django is not None:
            validation_data_django = self.django()
            validation_data.update({DJANGO: validation_data_django})

        return validation_data

    def python_magic(self):
        """Test."""
        load_dotenv()
        operating_system_name = platform.system()
        path_magic_file = os.environ.get("path_magic_file")
        if path_magic_file and operating_system_name == "Windows":
            with open(self.file_path, "rb") as file:
                magic.Magic(magic_file=path_magic_file)
                file_mime = magic.from_buffer(file.read(2048), mime=True)
        else:
            with open(self.file_path, "rb") as file:
                file_mime = magic.from_buffer(file.read(2048), mime=True)

        if file_mime not in self.acceptable_mimes:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime),
                    "red",
                ),
            )
        current_file = Path(self.file_path)
        file_type = file_mime.split("/")[0]
        file_name = current_file.name
        file_extension = current_file.suffix
        result_of_validation = generate_information_about_file(
            status=OK,
            library=PYTHON_MAGIC,
            file_name=file_name,
            file_mime=file_mime,
            file_type=file_type,
            file_extension=file_extension,
        )
        self.result_of_validation.update({PYTHON_MAGIC: result_of_validation})
        return result_of_validation

    def pure_magic(self):
        """Test."""
        try:
            with open(self.file_path, "rb") as file:
                file_signatures = puremagic.magic_stream(file)
                file_mimes = []
                for file_signature in file_signatures:
                    file_mimes.append(file_signature.mime_type)
        except PureError as error:
            raise FileValidationException(colored(MIME_NOT_VALID, "red")) from error

        file_mime = file_mimes[0]
        if file_mime not in self.acceptable_mimes:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime),
                    "red",
                ),
            )
        current_file = Path(self.file_path)
        file_type = file_mime.split("/")[0]
        result_of_validation = generate_information_about_file(
            status=OK,
            library=PURE_MAGIC,
            file_name=current_file.name,
            file_mime=file_mime,
            file_type=file_type,
            file_extension=current_file.suffix,
        )
        self.result_of_validation.update({PURE_MAGIC: result_of_validation})
        return result_of_validation

    def mimetypes(self):
        """Test."""
        file_mime = guess_type(self.file_path)[0]
        if file_mime is None:
            raise FileValidationException(colored(MIME_NOT_VALID, "red"))

        if file_mime not in self.acceptable_mimes:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime),
                    "red",
                ),
            )

        current_file = Path(self.file_path)
        file_type = file_mime.split("/")[0]
        result_of_validation = generate_information_about_file(
            status=OK,
            library=MIMETYPES,
            file_name=current_file.name,
            file_mime=file_mime,
            file_type=file_type,
            file_extension=current_file.suffix,
        )
        self.result_of_validation.update({MIMETYPES: result_of_validation})
        return result_of_validation

    def filetype(self):
        """Test."""
        try:
            file_mime = guess(self.file_path).MIME
        except AttributeError as error:
            raise FileValidationException(colored(MIME_NOT_VALID, "red")) from error

        if file_mime not in self.acceptable_mimes:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(file_mime=file_mime),
                    "red",
                ),
            )

        current_file = Path(self.file_path)
        file_type = file_mime.split("/")[0]
        result_of_validation = generate_information_about_file(
            status=OK,
            library=FILETYPE,
            file_name=current_file.name,
            file_mime=file_mime,
            file_type=file_type,
            file_extension=current_file.suffix,
        )
        self.result_of_validation.update({FILETYPE: result_of_validation})
        return result_of_validation

    def django(self):
        """Return."""
        if self.file_mime_guessed_by_django not in self.acceptable_mimes:
            raise FileValidationException(
                colored(
                    MIME_NOT_VALID_WITH_MIME_NAME.format(
                        file_mime=self.file_mime_guessed_by_django,
                    ),
                    "red",
                ),
            )
        current_file = Path(self.file_path)
        file_type = self.file_mime_guessed_by_django.split("/")[0]
        result_of_validation = generate_information_about_file(
            status=OK,
            file_name=current_file.name,
            file_mime=self.file_mime_guessed_by_django,
            file_type=file_type,
            file_extension=current_file.suffix,
        )
        self.result_of_validation.update({DJANGO: result_of_validation})
        return result_of_validation

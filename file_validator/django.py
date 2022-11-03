"""
In this module, there are file validators for Django,
and it is made using external libraries such as (filetype, python-magic)
and native libraries such as (mimetypes), and there is a method to perform
validation operations using all three libraries It is called safe mode
"""
from termcolor import colored

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

from .exceptions import error_message
from .constants import (
    FILE_SIZE_IS_NOT_VALID,
    MIMES_EMPTY,
    ZERO,
    ALL_SUPPORTED_LIBRARIES,
    SELECTING_ALL_SUPPORTED_LIBRARIES,
    LIBRARY_IS_NOT_SUPPORTED,
    PYTHON_MAGIC,
    PURE_MAGIC,
    FILETYPE,
    MIMETYPES,
)
from .validator import (
    file_validator,
    file_validator_by_python_magic,
    file_validator_by_pure_magic,
    file_validator_by_filetype,
    file_validator_by_mimetypes,
)


@deconstructible
class FileValidator:
    """
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(
        self,
        libraries: list = None,
        mimes: list = None,
        file_size: int = 0,
    ):

        """
        :type mimes: list

        :param mimes: The mimes you want the file to be checked based on, example: image/png

        :type file_size: int, optional

        :param file_size: If you want the file size to be checked, the file size must be in bytes,
            example: file_size=1048576 (1MB), defaults to 0, optional

        :type libraries: list, optional

        :param libraries: The value of libraries should be a list of libraries with which you
            want to perform the validation operation, example: libraries=["filetype","python_magic"]
            defaults If you do not select any library, it will perform the validation operation with
            all libraries by default, Supported libraries for validation operations: python_magic,
            pure_magic, filetype, mimetypes

        :raises ValueError: If the mime list is empty, raised a value error
        :raises ValueError: If the library you entered is not supported, raised a value error,
            Supported library: filetype, mimetypes, pure_magic, python_magic
        """
        if file_size != ZERO:
            self.file_size = file_size
        else:
            self.file_size = ZERO

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

        if mimes is None or not all(mimes):
            raise ValueError(colored(MIMES_EMPTY, "red"))

        self.mimes = []
        for mime in mimes:
            self.mimes.append(mime)

    def __call__(self, value):
        file = value.file
        file_size = file.size
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        if self.file_size != ZERO and file_size > self.file_size:
            raise ValidationError(
                error_message(
                    file=file,
                    mimes=self.mimes,
                    file_size=filesizeformat(file_size),
                    max_file_size=filesizeformat(self.file_size),
                    message=FILE_SIZE_IS_NOT_VALID,
                )
            )
        for library in self.libraries:
            try:
                if library == SELECTING_ALL_SUPPORTED_LIBRARIES:
                    file_validator(mimes=self.mimes, file_path=file_path)

                elif library == PYTHON_MAGIC:
                    file_validator_by_python_magic(
                        mimes=self.mimes, file_path=file_path
                    )

                elif library == PURE_MAGIC:
                    file_validator_by_pure_magic(
                        mimes=self.mimes, file_path=file_path
                    )

                elif library == FILETYPE:
                    file_validator_by_filetype(
                        mimes=self.mimes, file_path=file_path
                    )

                elif library == MIMETYPES:
                    file_validator_by_mimetypes(
                        mimes=self.mimes, file_path=file_path
                    )

            except ValueError as error:
                raise ValidationError(
                    error_message(
                        file=file,
                        file_size=filesizeformat(file_size),
                        max_file_size=filesizeformat(self.file_size),
                        mimes=self.mimes,
                    )
                ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.libraries == other.libraries
            and self.mimes == other.mimes
            and self.file_size == other.file_size
        )

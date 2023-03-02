"""
In this module, there are file validators and field for Django.
and it is made using external libraries such as (filetype, python-magic, pure_magic, mimetypes)
and native libraries such as (mimetypes), and there is a method to perform
validation operations using all three libraries It is called safe mode
"""

from django.db.models import FileField
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from termcolor import colored
from humanize import naturalsize

from file_validator.exceptions import (
    error_message,
    FileValidationException,
    MimesEmptyException,
    SizeValidationException,
)
from file_validator.utils import all_mimes_is_equal, is_library_supported
from file_validator.validators import size_validator, file_validator_by_django
from file_validator.constants import (
    MIMES_EMPTY,
    SELECTING_ALL_SUPPORTED_LIBRARIES,
    MAX_UPLOAD_SIZE_IS_EMPTY,
    FILE_SIZE_IS_NOT_VALID,
)


class ValidatedFileField(FileField):
    """
    :return: If everything is OK, it will return None, otherwise it will
        return a ValidationError.
    """

    def __init__(self, **kwargs):
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
            any library, it will perform the validation operation with django by
            default, Supported libraries for validation operations:
            python_magic, pure_magic, filetype, mimetypes, all, default
        :raises ValueError: If the mime list is empty, raised a value error
        :raises ValueError: If the library you entered is not supported,
            raised a value error, Supported library: filetype, mimetypes,
            pure_magic, python_magic
        :raises ValidationError: if file not valid
        """
        self.acceptable_mimes: list = kwargs.get("acceptable_mimes")
        if self.acceptable_mimes is None or all_mimes_is_equal(self.acceptable_mimes):
            raise MimesEmptyException(colored(MIMES_EMPTY, "red"))

        libraries: list = kwargs.get("libraries")
        self.libraries = []
        if libraries is None:
            self.libraries.append(SELECTING_ALL_SUPPORTED_LIBRARIES)
        else:
            for library in libraries:
                is_library_supported(library)
                self.libraries.append(library)

        self.max_upload_file_size: int = kwargs.get("max_upload_file_size")
        super().__init__()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["acceptable_mimes"] = self.acceptable_mimes
        kwargs["libraries"] = self.libraries
        kwargs["max_upload_file_size"] = self.max_upload_file_size
        return name, path, args, kwargs

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        current_file = data.file
        content_type_guessed_by_django = current_file.content_type
        file_size = current_file.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        try:
            file_size_validation_data = size_validator(
                max_upload_file_size=self.max_upload_file_size,
                file_path=file_path,
            )
            file_validation_data = file_validator_by_django(
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                file_path=file_path,
                content_type_guessed_by_django=content_type_guessed_by_django,
            )

        except (FileValidationException, SizeValidationException) as error:
            raise ValidationError(
                error_message(
                    mimes=self.acceptable_mimes,
                    file_name=current_file.name,
                    file_size=naturalsize(file_size),
                    max_file_size=naturalsize(self.max_upload_file_size)
                    if self.max_upload_file_size is not None
                    else 0,
                    current_file_mime=content_type_guessed_by_django,
                )
            ) from error
        setattr(
            data,
            "validation_data",
            {
                # merge two dictionaries
                **file_validation_data,
                **file_size_validation_data,
            },
        )
        return data


@deconstructible
class FileValidator:
    """
    file validator for django
    """

    def __init__(
        self,
        libraries: list = None,
        acceptable_mimes: list = None,
        max_upload_file_size: int = None,
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
            any library, it will perform the validation operation with django by
            default, Supported libraries for validation operations:
            python_magic, pure_magic, filetype, mimetypes, all, default
        :raises ValueError: If the mime list is empty, raised a value error
        :raises ValueError: If the library you entered is not supported,
            raised a value error, Supported library: filetype, mimetypes,
            pure_magic, python_magic
        :return: If everything is OK, it will return None, otherwise it will
            return a ValidationError.
        """
        if max_upload_file_size is not None:
            self.max_upload_file_size = max_upload_file_size
        else:
            self.max_upload_file_size = None

        self.libraries = []
        if libraries is None:
            self.libraries.append(SELECTING_ALL_SUPPORTED_LIBRARIES)
        else:
            for library in libraries:
                is_library_supported(library)
                self.libraries.append(library)

        if acceptable_mimes is None or all_mimes_is_equal(acceptable_mimes):
            raise MimesEmptyException(colored(MIMES_EMPTY, "red"))

        self.acceptable_mimes = []
        for mime in acceptable_mimes:
            self.acceptable_mimes.append(mime)

    def __call__(self, value):
        current_file = value.file
        file_size = current_file.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        content_type_guessed_by_django = current_file.content_type
        try:
            size_validator(
                max_upload_file_size=self.max_upload_file_size,
                file_path=file_path,
            )
            file_validator_by_django(
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                file_path=file_path,
                content_type_guessed_by_django=content_type_guessed_by_django,
            )
        except (FileValidationException, SizeValidationException) as error:
            raise ValidationError(
                error_message(
                    mimes=self.acceptable_mimes,
                    file_name=current_file.name,
                    file_size=naturalsize(file_size),
                    max_file_size=naturalsize(self.max_upload_file_size)
                    if self.max_upload_file_size is not None
                    else 0,
                    current_file_mime=content_type_guessed_by_django,
                )
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.libraries == other.libraries
            and self.acceptable_mimes == other.acceptable_mimes
            and self.max_upload_file_size == other.max_upload_file_size
        )

    def __hash__(self):
        return hash((self.max_upload_file_size, self.libraries, self.acceptable_mimes))


@deconstructible
class FileSizeValidator:
    """
    size validator for django
    """

    def __init__(
        self,
        max_upload_file_size: int = None,
    ):
        """
        :type max_upload_file_size: int
        :param max_upload_file_size: If you want the file size to be checked,
            the file size must be in bytes,
            example: file_size=1048576 (1MB), defaults to 0, optional
        :return: If everything is OK, it will return None, otherwise it will
            return a ValidationError.
        """
        if max_upload_file_size is None:
            raise SizeValidationException(colored(MAX_UPLOAD_SIZE_IS_EMPTY, "red"))

        self.max_upload_file_size = max_upload_file_size

    def __call__(self, value):
        current_file = value.file
        file_size = current_file.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        try:
            size_validator(
                max_upload_file_size=self.max_upload_file_size,
                file_path=file_path,
            )
        except SizeValidationException as error:
            raise ValidationError(
                error_message(
                    file_name=current_file.name,
                    file_size=naturalsize(file_size),
                    max_file_size=naturalsize(self.max_upload_file_size),
                    message=FILE_SIZE_IS_NOT_VALID,
                )
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.max_upload_file_size == other.max_upload_file_size
        )

    def __hash__(self):
        return hash(self.max_upload_file_size)

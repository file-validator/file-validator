"""In this module, there are file validators and field for Django.

and it is made using external libraries such as (filetype, python-magic,
pure_magic, mimetypes) and native libraries such as (mimetypes), and
there is a method to perform validation operations using all three
libraries It is called safe mode
"""

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import FileField
from django.utils.deconstruct import deconstructible
from humanize import naturalsize
from termcolor import colored

from file_validator.constants import (
    ALL,
    FILE_SIZE_IS_NOT_VALID,
    FILETYPE,
    MAX_UPLOAD_SIZE_IS_EMPTY,
    MIMETYPES,
    PURE_MAGIC,
    PYTHON_MAGIC,
)
from file_validator.exceptions import (
    error_message,
    FileValidationException,
    SizeValidationException,
)
from file_validator.utils import (
    all_mimes_is_equal,
    is_library_supported,
    is_type_supported,
    parameters_are_empty,
    set_the_acceptable_mimes,
    set_the_library,
)
from file_validator.validators import FileValidator


class ValidatedFileField(FileField):
    """
    :return: If everything is OK, it will return None, otherwise it will
        return a ValidationError.
    """

    def __init__(self, *args, **kwargs):
        """
        :type acceptable_mimes: list
        :param acceptable_mimes: The mimes you want the file to be checked
            based on, example: image/png
        :type acceptable_types: list
        :param acceptable_types: The types you want the file to be checked based on, example: font,
            audio, video, image, archive
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
        self.max_upload_file_size: int = kwargs.pop("max_upload_file_size", None)
        self.acceptable_mimes: list = kwargs.pop("acceptable_mimes", None)
        self.acceptable_types: list = kwargs.pop("acceptable_types", None)
        libraries: list = kwargs.pop("libraries", None)

        parameters_are_empty(
            acceptable_mimes=self.acceptable_mimes,
            acceptable_types=self.acceptable_types,
        )

        all_mimes_is_equal(self.acceptable_mimes)

        self.acceptable_mimes = set_the_acceptable_mimes(self.acceptable_mimes)

        self.libraries = set_the_library(libraries)

        is_type_supported(acceptable_types=self.acceptable_types)

        super(ValidatedFileField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["acceptable_mimes"] = self.acceptable_mimes
        kwargs["acceptable_types"] = self.acceptable_types
        kwargs["libraries"] = self.libraries
        kwargs["max_upload_file_size"] = self.max_upload_file_size
        return name, path, args, kwargs

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        current_file = data.file
        try:
            file_mime_guessed_by_django = current_file.content_type
        except AttributeError:
            file_mime_guessed_by_django = None
        file_size = data.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        try:
            file_validator = FileValidator(
                file_path=file_path,
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                acceptable_types=self.acceptable_types,
                max_upload_file_size=self.max_upload_file_size,
                file_mime_guessed_by_django=file_mime_guessed_by_django,
            )
            if self.acceptable_mimes is not None:
                for library in self.libraries:
                    if library == ALL:
                        file_validator.validate()
                    elif library == PYTHON_MAGIC:
                        file_validator.python_magic()
                    elif library == PURE_MAGIC:
                        file_validator.pure_magic()
                    elif library == MIMETYPES:
                        file_validator.mimetypes()
                    elif library == FILETYPE:
                        file_validator.filetype()
                    else:
                        file_validator.django()
            if self.acceptable_types is not None:
                file_validator.validate_type()
            if self.max_upload_file_size is not None:
                file_validator.validate_size()
        except (FileValidationException, SizeValidationException) as error:
            raise ValidationError(
                error_message(
                    acceptable_mimes=self.acceptable_mimes,
                    acceptable_types=self.acceptable_types,
                    current_file_name=current_file.name,
                    current_file_size=naturalsize(file_size),
                    current_file_mime=file_mime_guessed_by_django,
                    max_file_size=naturalsize(self.max_upload_file_size)
                    if self.max_upload_file_size is not None
                    else 0,
                ),
            ) from error
        setattr(data, "validation_data", file_validator.result_of_validation)
        return data


@deconstructible
class DjangoFileValidator:
    """File validator for django."""

    def __init__(
        self,
        libraries: list = None,
        acceptable_mimes: list = None,
        acceptable_types: list = None,
        max_upload_file_size: int = None,
    ):
        """
        :type acceptable_mimes: list
        :param acceptable_mimes: The mimes you want the file to be checked
            based on, example: image/png
        :type acceptable_types: list
        :param acceptable_types: The types you want the file to be checked based on, example: font,
            audio, video, image, archive
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
        self.max_upload_file_size = None
        self.acceptable_types: list = acceptable_types
        self.libraries = set_the_library(libraries)

        if max_upload_file_size is not None:
            self.max_upload_file_size = max_upload_file_size

        parameters_are_empty(
            acceptable_mimes=acceptable_mimes,
            acceptable_types=acceptable_types,
        )

        all_mimes_is_equal(acceptable_mimes)

        self.acceptable_mimes = set_the_acceptable_mimes(acceptable_mimes)

        is_type_supported(acceptable_types=self.acceptable_types)

    def __call__(self, value):
        current_file = value.file
        file_size = value.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        try:
            file_mime_guessed_by_django = current_file.content_type
        except AttributeError:
            file_mime_guessed_by_django = None
        try:
            file_validator = FileValidator(
                file_path=file_path,
                libraries=self.libraries,
                acceptable_mimes=self.acceptable_mimes,
                acceptable_types=self.acceptable_types,
                max_upload_file_size=self.max_upload_file_size,
                file_mime_guessed_by_django=file_mime_guessed_by_django,
            )
            if self.acceptable_mimes is not None:
                for library in self.libraries:
                    is_library_supported(library)
                    if library == ALL:
                        file_validator.validate()
                    elif library == PYTHON_MAGIC:
                        file_validator.python_magic()
                    elif library == PURE_MAGIC:
                        file_validator.pure_magic()
                    elif library == MIMETYPES:
                        file_validator.mimetypes()
                    elif library == FILETYPE:
                        file_validator.filetype()
                    else:
                        file_validator.django()
            if self.acceptable_types is not None:
                file_validator.validate_type()
            if self.max_upload_file_size is not None:
                file_validator.validate_size()
        except (FileValidationException, SizeValidationException) as error:
            raise ValidationError(
                error_message(
                    acceptable_mimes=self.acceptable_mimes,
                    acceptable_types=self.acceptable_types,
                    current_file_name=current_file.name,
                    current_file_size=naturalsize(file_size),
                    current_file_mime=file_mime_guessed_by_django,
                    max_file_size=naturalsize(self.max_upload_file_size)
                    if self.max_upload_file_size is not None
                    else 0,
                ),
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.libraries == other.libraries
            and self.acceptable_mimes == other.acceptable_mimes
            and self.acceptable_types == other.acceptable_types
            and self.max_upload_file_size == other.max_upload_file_size
        )

    def __hash__(self):
        return hash(self.max_upload_file_size)


@deconstructible
class FileSizeValidator:
    """Size validator for django."""

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
        file_size = value.size
        file_path = TemporaryUploadedFile.temporary_file_path(current_file)
        try:
            file_validator = FileValidator(
                file_path=file_path,
                max_upload_file_size=self.max_upload_file_size,
            )
            file_validator.validate_size()
        except SizeValidationException as error:
            raise ValidationError(
                error_message(
                    current_file_name=current_file.name,
                    current_file_size=naturalsize(file_size),
                    max_file_size=naturalsize(self.max_upload_file_size),
                    message=FILE_SIZE_IS_NOT_VALID,
                ),
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.max_upload_file_size == other.max_upload_file_size
        )

    def __hash__(self):
        return hash(self.max_upload_file_size)

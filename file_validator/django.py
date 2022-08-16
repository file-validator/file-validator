"""
In this module, there are file validators for Django,
and it is made using external libraries such as (filetype, python-magic)
and native libraries such as (mimetypes), and there is a method to perform
validation operations using all three libraries It is called safe mode
"""

from mimetypes import guess_extension, guess_type
import magic
from filetype import get_type, guess, is_mime_supported
from termcolor import colored
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.deconstruct import deconstructible


from .exceptions import (
    error_message,
    ARGS_EMPTY_ERROR_MESSAGE,
    MIME_NOT_VALID_ERROR_MESSAGE,
)


@deconstructible
class FileValidatorByPythonMagic:
    """
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(self, mimes: list):
        """
        :param mimes: The mimes you want the file to be checked based on
        """
        if not all(mimes):
            message = ARGS_EMPTY_ERROR_MESSAGE
            raise ValueError(colored(message, "red"))
        self.selected_mimes = []
        for mime in mimes:
            self.selected_mimes.append(mime)

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        with open(file_path, "rb") as file_object:
            file_mime = magic.from_buffer(file_object.read(2048), mime=True)
        if file_mime not in self.selected_mimes:
            raise ValidationError(error_message(file=file, mimes=self.selected_mimes))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.selected_mimes == other.selected_mimes
        )


@deconstructible
class FileValidatorByMimeTypes:
    """
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(self, mimes: list):
        """
        :param mimes: The mimes you want the file to be checked based on
        """
        self.selected_mimes = mimes
        self.selected_extensions = []
        for mime in mimes:
            file_extension = guess_extension(mime)
            if file_extension is not None:
                self.selected_extensions.append(file_extension)
            else:
                message = MIME_NOT_VALID_ERROR_MESSAGE.format(mime=mime)
                raise ValueError(colored(message, "red"))

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        try:
            file_mime = guess_type(file_path)[0]
            file_extension = guess_extension(file_mime)
            if (
                file_mime not in self.selected_mimes
                or file_extension not in self.selected_extensions
            ):
                raise ValidationError(
                    error_message(file=file, mimes=self.selected_mimes)
                )
        except AttributeError as error:
            raise ValidationError(
                error_message(file=file, mimes=self.selected_mimes)
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.selected_mimes == other.selected_mimes
            and self.selected_extensions == other.selected_extensions
        )


@deconstructible
class FileValidatorByFileType:
    """
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(self, mimes: list):
        """
        :param mimes: The mimes you want the file to be checked based on
        :raises ValueError: If the type you enter is not supported, it will cause this value error
        """
        if not all(mimes):
            message = ARGS_EMPTY_ERROR_MESSAGE
            raise ValueError(colored(message, "red"))
        self.selected_mimes = []
        self.selected_extensions = []
        for selected_file_type in mimes:
            if is_mime_supported(selected_file_type):
                file_object = get_type(mime=selected_file_type)
                self.selected_mimes.append(file_object.MIME)
                self.selected_extensions.append(file_object.EXTENSION)
            else:
                message = MIME_NOT_VALID_ERROR_MESSAGE.format(mime=selected_file_type)
                raise ValueError(colored(message, "red"))

    def __call__(self, value):
        """
        :param value: Here, value means the file that is received by the user and must be validated
        """
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        try:
            current_file = guess(file_path)
            if (
                current_file.EXTENSION not in self.selected_extensions
                and current_file.MIME not in self.selected_mimes
            ):
                raise ValidationError(
                    error_message(file=file, mimes=self.selected_mimes)
                )
        except AttributeError as error:
            raise ValidationError(
                error_message(file=file, mimes=self.selected_mimes)
            ) from error

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.selected_mimes == other.selected_mimes
            and self.selected_extensions == other.selected_extensions
        )


@deconstructible
class FileValidator:
    """
    :return: If everything is OK it will return None, otherwise it will return a ValidationError.
    """

    def __init__(self, mimes: list, python_magic: bool = False):
        """
        :param mimes: The mimes you want the file to be checked based on
        :param python_magic: If it is equal to True, the file will be checked with python-magic
        """
        selected_mimes = []
        for mime in mimes:
            if is_mime_supported(mime):
                file_object = get_type(mime=mime)
                selected_mimes.append(file_object.MIME)
            else:
                message = MIME_NOT_VALID_ERROR_MESSAGE.format(mime=mime)
                raise ValueError(colored(message, "red"))
        self.selected_mimes = selected_mimes
        self.must_be_validated_by_pg: bool = python_magic

    def __call__(self, value):
        file = value.file
        file_path = TemporaryUploadedFile.temporary_file_path(file)
        with open(file_path, "rb") as file_object:
            file_mime_with_pg = magic.from_buffer(
                file_object.read(2048), mime=True
            )  # get file mime use Python Magic (pg) library
        file_mime_with_filetype = guess(
            file_path
        ).MIME  # get file mime use filetype library
        file_mime_with_mimetypes = guess_type(file_path)[
            0
        ]  # get the file mime use mimetypes library (native in python)
        if self.must_be_validated_by_pg:
            if (
                file_mime_with_filetype not in self.selected_mimes
                or file_mime_with_mimetypes not in self.selected_mimes
                or file_mime_with_pg not in self.selected_mimes
            ):
                raise ValidationError(
                    error_message(file=file, mimes=self.selected_mimes)
                )
        else:
            if (
                file_mime_with_filetype not in self.selected_mimes
                or file_mime_with_mimetypes not in self.selected_mimes
            ):
                raise ValidationError(
                    error_message(file=file, mimes=self.selected_mimes)
                )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.selected_mimes == other.selected_mimes
            and self.must_be_validated_by_pg == other.must_be_validated_by_pg
        )

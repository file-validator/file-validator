"""This file is for customizing errors and anything related to errors."""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from file_validator.constants import DEFAULT_ERROR_MESSAGE, DEFAULT_FILE_NAME

try:
    # Get Error Message From Django Setting
    CUSTOM_ERROR_MESSAGE = settings.FILE_VALIDATOR_ERROR_MESSAGE
except (AttributeError, ImproperlyConfigured):
    CUSTOM_ERROR_MESSAGE = DEFAULT_ERROR_MESSAGE


class FileValidationException(Exception):
    """Raised when file is not valid."""


class SizeValidationException(Exception):
    """Raised when file size is not valid."""


class DjangoFileValidationException(Exception):
    """Raised when file validation operation for django fails."""


class LibraryNotSupportedException(Exception):
    """Raised when a library is not supported."""


class MimesEmptyException(Exception):
    """Raised when the mime list is empty."""


class MimesEqualException(Exception):
    """Raised when the mime list is empty."""


class TypeNotSupportedException(Exception):
    """Raised when the type not supported, supported types: image, audio,
    video, archive, font."""


class EmptyParametersException(Exception):
    """Raised when the type not supported, supported types: image, audio,
    video, archive, font."""


def convert_list_to_readable_string(object_list) -> str:
    """Convert a list of objects to a readable string."""
    result = ""
    for value in object_list:
        if value == object_list[-1]:
            result += str(value)
        else:
            result += str(value)
            result += ", "
    return result


def error_message(
    current_file_extension=None,
    current_file_name=DEFAULT_FILE_NAME,
    current_file_size=None,
    current_file_mime=None,
    current_file_type=None,
    **kwargs
) -> str:
    """:type current_file_name: str :param current_file_name: Returns the name
    of the file to be validated :type current_file_mime: list :param
    current_file_mime: It returns current file mime :type current_file_type:
    str :param current_file_type: It returns the file size on which the file is
    to be validated :type current_file_size: str :param current_file_size: It
    returns the file size on which the file is to be validated :type
    current_file_extension: str :param current_file_extension: It returns
    current file extention If you have not confirmed the file size, it will
    return 0 by default :param message: The error message to be shown to the
    user when the file is not valid :return: return your error message or
    default error message."""
    file_mimes = None
    file_types = None
    file_extensions = None
    message = kwargs.get("message")
    max_file_size = kwargs.get("max_file_size")
    acceptable_mimes = kwargs.get("acceptable_mimes")
    acceptable_types = kwargs.get("acceptable_types")
    acceptable_extensions = kwargs.get("acceptable_extensions")

    if message is None:
        message = CUSTOM_ERROR_MESSAGE

    if acceptable_extensions is not None:
        file_extensions = convert_list_to_readable_string(
            object_list=acceptable_extensions,
        )

    if acceptable_types is not None:
        file_types = convert_list_to_readable_string(object_list=acceptable_types)

    if acceptable_mimes is not None:
        file_mimes = convert_list_to_readable_string(object_list=acceptable_mimes)

    return message.format(
        max_file_size=max_file_size,
        acceptable_mimes=file_mimes,
        acceptable_types=file_types,
        acceptable_extensions=file_extensions,
        current_file_size=current_file_size,
        current_file_name=current_file_name,
        current_file_mime=current_file_mime,
        current_file_type=current_file_type,
        current_file_extension=current_file_extension,
    )

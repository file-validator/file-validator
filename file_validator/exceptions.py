"""
This file is for customizing errors and anything related to errors
"""
from django.conf import settings

try:
    ERROR_MESSAGE = settings.FILE_VALIDATOR_ERROR_MESSAGE
except AttributeError:
    ERROR_MESSAGE = "{file} is not valid"


def error_message(
    file,
    mimes,
    file_size,
    max_file_size,
    message=ERROR_MESSAGE,
):
    """
    :param file: Returns the name of the file to be validated
    :param mimes: It returns the mimes on which the file is to be validated
    :param file_size: It returns the file size on which the file is to be validated
    :param max_file_size: Returns the maximum file size to be validated and the user can upload,
        If you have not confirmed the file size, it will return 0 by default
    :param message: The error message to be shown to the user when the file is not valid
    :return: return your error message or default error message
    """
    file_mimes = ""
    for mime in mimes:
        if mime == mimes[-1]:
            file_mimes += str(mime)
        else:
            file_mimes += str(mime)
            file_mimes += ", "

    return message.format(
        file=file, mimes=file_mimes, file_size=file_size, max_file_size=max_file_size
    )

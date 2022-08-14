from django.conf import settings
from termcolor import colored

try:
    ERROR_MESSAGE = settings.FILE_VALIDATOR_ERROR_MESSAGE
except AttributeError:
    ERROR_MESSAGE = "{file} is not valid"


def error_message(
    file,
    mimes,
    message=ERROR_MESSAGE,
):
    """
    :param file: Returns the name of the file to be validated
    :param mimes: It returns the mimes on which the file is to be validated
    :param message: The error message to be shown to the user when the file is not valid,
    You can customize this message through the Django settings (settings.py), to display
    the file name in the error message, just put the string {file} in the error message
    you want, or to display the mimes that the file is based on To be validated,
    just put {mimes} in your error message
    :return: In case of customization, it will return your error message, and otherwise it will return "{file} is not valid" message.
    """
    file_mimes = ""
    for mime in mimes:
        file_mimes += str(mime)
        file_mimes += ', '
        if mime == mimes[-1]:
            file_mimes += str(mime)
    return message.format(file=file, mimes=file_mimes)

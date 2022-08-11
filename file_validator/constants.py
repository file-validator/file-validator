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
    file_mimes = ""
    for mime in mimes:
        file_mimes += str(mime)
        file_mimes += ', '
        if mime == mimes[-1]:
            file_mimes += str(mime)
    return message.format(file=file, mimes=file_mimes)

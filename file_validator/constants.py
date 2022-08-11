from django.conf import settings
from termcolor import colored

FILE_VALIDATOR_ERROR_MESSAGE = settings.FILE_VALIDATOR_ERROR_MESSAGE
FILE_VALIDATOR_SHOW_MESSAGE_ONLY = settings.FILE_VALIDATOR_SHOW_MESSAGE_ONLY
FILE_VALIDATOR_SHOW_FILE_NAME = settings.FILE_VALIDATOR_SHOW_FILE_NAME
FILE_VALIDATOR_SHOW_MIME_TYPE = settings.FILE_VALIDATOR_SHOW_MIME_TYPE

if FILE_VALIDATOR_SHOW_MIME_TYPE:
    SHOW_MIME_TYPE = True
else:
    SHOW_MIME_TYPE = False

if FILE_VALIDATOR_SHOW_FILE_NAME:
    SHOW_FILE_NAME = True
else:
    SHOW_FILE_NAME = False

if FILE_VALIDATOR_SHOW_MESSAGE_ONLY:
    SHOW_MESSAGE_ONLY = True
else:
    SHOW_MESSAGE_ONLY = False

if FILE_VALIDATOR_ERROR_MESSAGE:
    ERROR_MESSAGE = FILE_VALIDATOR_ERROR_MESSAGE
else:
    ERROR_MESSAGE = "The file is not valid"


def error_message(
    file,
    mimes,
    message=ERROR_MESSAGE,
    show_file_name=SHOW_FILE_NAME,
    show_mime_type=SHOW_MIME_TYPE,
    show_message_only=SHOW_MESSAGE_ONLY,
):
    if (
        show_file_name
        and show_mime_type
        and show_message_only
        or show_mime_type
        and show_message_only
        or show_file_name
        and show_message_only
    ):
        message = "If you want only the message to be displayed, set the show_file_name and show_mime_type parameters to False"
        raise ValueError(colored(message, "red"))

    file_mimes = ""
    for mime in mimes:
        file_mimes += str(mime)
        file_mimes += ', '
        if mime == mimes[-1]:
            file_mimes += str(mime)

    if show_file_name:
        message = f"{file} {message}"
    elif show_mime_type:
        message = f"{message} {file_mimes}"
    elif show_file_name and show_mime_type:
        message = f"{file} {message} {file_mimes}"
    elif show_message_only:
        message = f"{message}"
    else:
        message = f"{file} {message} {file_mimes}"
    return message

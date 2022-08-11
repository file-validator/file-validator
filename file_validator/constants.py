from termcolor import colored

ERROR_MESSAGE = "file is not valid"


def error_message(
    file,
    message,
    mimes,
    show_file_name=False,
    show_mime_type=False,
    show_message_only=False,
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

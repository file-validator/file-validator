from filetype import guess
from mimetypes import guess_type
from termcolor import colored
import magic


def file_validator_by_python_magic(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png, video/mp4
    :return: If everything goes well and is ok and the file matches the mimes you specified, it will return None, otherwise it will return a ValueError.
    """
    file_mime = magic.from_buffer(open(file_path, "rb").read(2048), mime=True)
    if file_mime not in list(args):
        error_message = f"""
        {file_mime} is not valid
        """
        raise ValueError(colored(error_message, "red"))


def file_validator_by_mimetypes(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png, video/mp4
    :return: If everything goes well and is ok and the file matches the mimes you specified, it will return None, otherwise it will return a ValueError.

    """
    file_mime = guess_type(file_path)[0]
    if file_mime not in list(args):
        error_message = f"""
        {file_mime} is not valid
        """
        raise ValueError(colored(error_message, "red"))


def file_validator_by_filetype(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example : image/png, video/mp4, audio/mpeg ...
    :return: If everything goes well and is ok and the file matches the mimes you specified, it will return None, otherwise it will return a ValueError.
    """
    file_mime = guess(file_path).MIME
    if file_mime not in list(args):
        error_message = f"{file_mime} is not valid"
        raise ValueError(colored(error_message, "red"))


def file_validator(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The mime of the files you want to validate based on them, example: image/png, video/mp4
    :return: If everything goes well and is ok and the file matches the mimes you specified, it will return None, otherwise it will return a ValueError.

    """
    file_validator_by_filetype(*args, file_path=file_path)
    file_validator_by_mimetypes(*args, file_path=file_path)
    file_validator_by_python_magic(*args, file_path=file_path)

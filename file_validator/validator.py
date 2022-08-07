from filetype import guess, is_mime_supported, is_extension_supported
import magic
import mimetypes
from termcolor import colored


def get_mime_type_with_python_magic(file_path):
    """
    :type file_path: string
    :param file_path: The path of the file you want to get MIME use python magic library
    :return: return MIME of file you gave it
    """
    file_mime = magic.from_buffer(open(file_path, "rb").read(2048), mime=True)
    return file_mime


def get_extension_with_filetype_lib(file_path):
    """
    :type file_path: string
    :param file_path: The path of the file you want to get the extension use filetype library
    :return: return extension of file you gave it
    """
    file_extension = guess(file_path).EXTENSION
    return file_extension


def get_mime_type_with_filetype_lib(file_path):
    """
    :type file_path: string
    :param file_path: The path of the file you want to get MIME use filetype library
    :return: return MIME of file you gave it
    """
    file_mime = guess(file_path).MIME
    return file_mime


def file_validator_with_filetype_lib(*args, file_path):
    """
    :type file_path: string
    :param file_path: The path to the file you want to validate
    :param args: The extension of the files you want to validate based on them
    """
    file_mime = get_mime_type_with_filetype_lib(file_path)
    file_extension = get_extension_with_filetype_lib(file_path)
    if is_extension_supported(file_extension):
        if file_mime not in list(args):
            error_message = f"""
            {file_mime} is not valid
            """
            raise ValueError(colored(error_message, "red"))

    else:
        error_message = f"""
        {file_extension} is not supported
        """
        raise ValueError(colored(error_message, "red"))

